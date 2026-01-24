import cv2
import os
import mido
import tkinter
import argparse
import sys


def preprocess_frame(frame):
    """Complete preprocessing pipeline for a single frame"""
    # Resize to 16x16
    resized = cv2.resize(frame, (16, 16), cv2.INTER_LINEAR)
    # Convert to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # Binarize using OTSU thresholding
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary


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

    # Calculate checksum
    sysex_sum = sum(sysex_list)
    checksum = 128 - (17 + sysex_sum) % 128
    if checksum == 128:
        checksum = 0

    return sysex_list, [checksum]


def video_to_image_list(video, frameskip):
    """
    Extract frames from video and process into binarized image list

    Parameters:
        video: Video object
        frameskip: Number of frames to skip after processing one frame

    Returns:
        List of processed binarized images
    """
    current_frame = 0
    frame_image_list = []

    while True:
        ret, frame_image = video.read()
        if not ret:
            break

        # Process frame if current_frame is divisible by (frameskip + 1)
        if current_frame % (frameskip + 1) == 0:
            processed_frame = preprocess_frame(frame_image)
            frame_image_list.append(processed_frame)

        current_frame += 1

    video.release()
    return frame_image_list


def create_sysex_messages(sysex_data, checksum, video_fps, frameskip):
    """Create all SysEx messages for a single frame"""
    messages = []

    # Main image data message
    image_sysex = [0x41, 0x10, 0x45, 0x12, 0x10, 0x01, 0x00] + sysex_data + checksum

    # Calculate time based on video FPS and frameskip
    # Each frame should be displayed for (frameskip + 1) / video_fps seconds
    # Convert to MIDI ticks (assuming 480 ticks per quarter note and tempo 500000)
    # 500000 microseconds per quarter note = 0.5 seconds per quarter note
    # So 480 ticks per 0.5 seconds = 960 ticks per second
    # Time per frame in seconds: (frameskip + 1) / video_fps
    # Time in ticks: 960 * (frameskip + 1) / video_fps
    time_per_frame_ticks = int(960 * (frameskip + 1) / video_fps)

    # Split time between messages (main message gets half, control messages get quarter each)
    messages.append(
        mido.Message(
            "sysex",
            data=image_sysex,
            time=time_per_frame_ticks // 2,
        )
    )

    # Additional control messages
    control_messages = [
        [0x41, 0x10, 0x45, 0x12, 0x10, 0x20, 0x00, 0x01, 0x4F],
        [0x41, 0x10, 0x45, 0x12, 0x10, 0x20, 0x01, 0x01, 0x4E],
    ]

    for data in control_messages:
        messages.append(
            mido.Message(
                "sysex",
                data=data,
                time=time_per_frame_ticks // 4,
            )
        )

    return messages


def pnglist_to_midifile(frame_image_list, video_fps, frameskip):
    """
    Convert binarized image list to MIDI file

    Parameters:
        frame_image_list: List of binarized images
        video_fps: Original video frame rate
        frameskip: Number of frames skipped between processed frames

    Returns:
        Generated MIDI file object
    """
    midifile = mido.MidiFile()
    meta_track = mido.MidiTrack()
    data_track = mido.MidiTrack()

    # Set tempo for MIDI file (500000 microseconds per quarter note = 120 BPM)
    meta_track.append(mido.MetaMessage("set_tempo", tempo=500000))

    for image in frame_image_list:
        # Calculate SysEx data
        sysex_data, checksum = calculate_sysex_data(image)

        # Create and add all SysEx messages for this frame
        sysex_messages = create_sysex_messages(
            sysex_data, checksum, video_fps, frameskip
        )
        for message in sysex_messages:
            data_track.append(message)

    # Combine all tracks
    midifile.tracks.append(meta_track)
    midifile.tracks.append(data_track)
    return midifile


def process(videofile, frameskip):
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

    frame_image_list = video_to_image_list(video, frameskip)
    midifile = pnglist_to_midifile(frame_image_list, video_fps, frameskip)

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
        "--frameskip",
        type=int,
        default=0,
        help="Number of frames to skip after processing one frame (default: 0)",
    )

    args = parser.parse_args()

    # Call the processing function with command line arguments
    process(args.input_video, args.frameskip)
