import cv2
import os
import mido
import tkinter
import argparse
import sys


def preprocess_frame(frame, resolution):
    """Complete preprocessing pipeline for a single frame"""
    # Resize
    resized = cv2.resize(frame, resolution, cv2.INTER_LINEAR)
    # Convert to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # Binarize using OTSU thresholding
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary


def video_to_image_list(video, frameskip, sc8850):
    """
    Extract frames from video and process into binarized image list

    Parameters:
        video: Video object
        frameskip: Number of frames to skip after processing one frame
        sc8850: Whether to enable SC-8850 mode

    Returns:
        List of processed binarized images
    """
    current_frame = 0
    frame_image_list = []

    if sc8850:
        target_resolution = (160, 64)
    else:
        target_resolution = (16, 16)

    while True:
        ret, frame_image = video.read()
        if not ret:
            break

        # Process frame if current_frame is divisible by (frameskip + 1)
        if current_frame % (frameskip + 1) == 0:
            processed_frame = preprocess_frame(frame_image, target_resolution)
            frame_image_list.append(processed_frame)

        current_frame += 1

    video.release()
    return frame_image_list


def convert_pixel_values(image):
    """
    Convert pixel values: 0->1, 255->0
    """
    image_list = image.tolist()
    return [[1 if pixel == 0 else 0 for pixel in row] for row in image_list]


def calculate_sysex_data(binary_image):
    """
    Convert 16x16 binary image to SysEx data format
    Returns the sysex list and checksum
    """
    # Convert to 0/1 representation
    binary_data = convert_pixel_values(binary_image)

    # Convert to SysEx format
    sysex_list = []

    # Process first 15 columns in groups of 5
    for col_start in [0, 5, 10]:
        for row in range(16):
            value = (
                16 * binary_data[row][col_start + 0]
                + 8 * binary_data[row][col_start + 1]
                + 4 * binary_data[row][col_start + 2]
                + 2 * binary_data[row][col_start + 3]
                + 1 * binary_data[row][col_start + 4]
            )
            sysex_list.append(value)

    # Process 16th column separately
    for row in range(16):
        sysex_list.append(16 * binary_data[row][15])

    return sysex_list


def calculate_sysex_data_8850(binary_image):
    """
    Convert 160x64 binary image to SysEx data format
    Returns the sysex list and checksum
    """
    # Convert to 0/1 representation
    binary_data = convert_pixel_values(binary_image)

    # Convert to SysEx format
    sysex_list = []

    for section in range(16):
        sysex_list.append([])
        for row in range(section * 4, section * 4 + 4):
            # Process first 156 columns in groups of 6
            for col_start in range(0, 156, 6):
                value = (
                    32 * binary_data[row][col_start + 0]
                    + 16 * binary_data[row][col_start + 1]
                    + 8 * binary_data[row][col_start + 2]
                    + 4 * binary_data[row][col_start + 3]
                    + 2 * binary_data[row][col_start + 4]
                    + 1 * binary_data[row][col_start + 5]
                )
                sysex_list[section].append(value)
            # Process 157+
            col_start = 156
            value = (
                32 * binary_data[row][col_start + 0]
                + 16 * binary_data[row][col_start + 1]
                + 8 * binary_data[row][col_start + 2]
                + 4 * binary_data[row][col_start + 3]
            )
            sysex_list[section].append(value)

    return sysex_list


def create_sysex_messages(sysex_data, video_fps, frameskip, framecount, sysex_address):
    """Create all SysEx messages for a single frame"""
    messages = []
    sysex_header = [0x41, 0x10, 0x45, 0x12]

    # Calculate checksum
    checksum = 128 - (sum(sysex_address) + sum(sysex_data)) % 128
    if checksum == 128:
        checksum = 0

    # Main image data message
    image_sysex = sysex_header + sysex_address + sysex_data + [checksum]

    # Calculate time based on video FPS and frameskip
    # Convert to MIDI ticks (assuming 480 ticks per quarter note and tempo 500000)
    # 500000 microseconds per quarter note = 0.5 seconds per quarter note
    # So 480 ticks per 0.5 seconds = 960 ticks per second
    frame_time = framecount * (frameskip + 1) / video_fps
    frame_next_time = (framecount + 1) * (frameskip + 1) / video_fps
    frame_tick = int(frame_time * 960)
    frame_next_tick = int(frame_next_time * 960)

    frame_length_tick = frame_next_tick - frame_tick

    messages.append(
        mido.Message(
            "sysex",
            data=image_sysex,
            time=frame_length_tick,
        )
    )

    return messages


def create_sysex_messages_8850(
    sysex_data, video_fps, frameskip, framecount, sysex_address, section
):
    """Create all SysEx messages for a single frame"""
    messages = []
    sysex_header = [0x41, 0x10, 0x45, 0x12]

    # Calculate checksum
    checksum = 128 - (sum(sysex_address) + sum(sysex_data)) % 128
    if checksum == 128:
        checksum = 0

    # Main image data message
    image_sysex = sysex_header + sysex_address + sysex_data + [checksum]

    # Calculate time based on video FPS and frameskip
    # Convert to MIDI ticks (assuming 480 ticks per quarter note and tempo 500000)
    # 500000 microseconds per quarter note = 0.5 seconds per quarter note
    # So 480 ticks per 0.5 seconds = 960 ticks per second
    frame_time = framecount * (frameskip + 1) / video_fps
    section_time = section / 16 / (video_fps / (frameskip + 1)) + frame_time
    section_next_time = (section + 1) / 16 / (video_fps / (frameskip + 1)) + frame_time
    section_tick = int(section_time * 960)
    section_next_tick = int(section_next_time * 960)

    section_length_tick = section_next_tick - section_tick

    messages.append(
        mido.Message(
            "sysex",
            data=image_sysex,
            time=section_length_tick,
        )
    )
    return messages


def image_list_to_midifile(frame_image_list, video_fps, frameskip, sc8850):
    """
    Convert binarized image list to MIDI file

    Parameters:
        frame_image_list: List of binarized images
        video_fps: Original video frame rate
        frameskip: Number of frames skipped between processed frames
        sc8850: Whether to enable SC-8850 mode

    Returns:
        Generated MIDI file object
    """
    midifile = mido.MidiFile()
    meta_track = mido.MidiTrack()
    data_track = mido.MidiTrack()

    # Set tempo for MIDI file (500000 microseconds per quarter note = 120 BPM)
    meta_track.append(mido.MetaMessage("set_tempo", tempo=500000))

    for framecount in range(len(frame_image_list)):
        image = frame_image_list[framecount]

        # Calculate SysEx data
        if sc8850:
            sysex_messages = []
            sysex_data = calculate_sysex_data_8850(image)
            for section in range(16):
                sysex_address = [0x20, section, 0x00]
                sysex_messages += create_sysex_messages_8850(
                    sysex_data[section],
                    video_fps,
                    frameskip,
                    framecount,
                    sysex_address,
                    section,
                )
            for message in sysex_messages:
                data_track.append(message)
        else:
            sysex_address = [0x10, 0x01, 0x00]
            sysex_data = calculate_sysex_data(image)
            # Create and add all SysEx messages for this frame
            sysex_messages = create_sysex_messages(
                sysex_data, video_fps, frameskip, framecount, sysex_address
            )
            for message in sysex_messages:
                data_track.append(message)

    # Combine all tracks
    midifile.tracks.append(meta_track)
    midifile.tracks.append(data_track)
    return midifile


def process(videofile, frameskip, sc8850):
    """
    Main processing function: Convert video file to MIDI file

    Parameters:
        videofile: Path to video file
        frameskip: Number of frames to skip after processing one frame
    """
    if not os.path.exists(videofile):
        print(f"Error: File '{videofile}' does not exist.")
        sys.exit(1)
    video = cv2.VideoCapture(videofile)
    video_fps = video.get(cv2.CAP_PROP_FPS)
    print(f"Video FPS: {video_fps}")
    print(f"Frameskip: {frameskip}")
    print(f"Effective frame rate: {video_fps / (frameskip + 1):.2f} FPS")

    frame_image_list = video_to_image_list(video, frameskip, sc8850)
    midifile = image_list_to_midifile(frame_image_list, video_fps, frameskip, sc8850)

    # Create output filename
    base_name = os.path.splitext(videofile)[0]
    output_file = f"{base_name}_skip{frameskip}.mid"
    midifile.save(output_file)
    print(f"Processed {len(frame_image_list)} frames")
    print(f"MIDI file saved as: {output_file}")


if __name__ == "__main__":
    # Setup command line argument parsing
    parser = argparse.ArgumentParser(
        description="Convert videos to MIDI files which can be read by Roland Sound Canvas."
    )
    parser.add_argument("input_video", type=str, help="Path to the input video file")
    parser.add_argument(
        "-f",
        "--frameskip",
        type=int,
        default=0,
        help="Number of frames to skip after processing one frame (default: 0)",
    )
    parser.add_argument(
        "-s",
        "--sc8850",
        action="store_true",
        help="Whether to enable SC-8850 mode, which enables higher resolution on compatible machines",
    )

    args = parser.parse_args()

    # Call the processing function with command line arguments
    process(args.input_video, args.frameskip, args.sc8850)
