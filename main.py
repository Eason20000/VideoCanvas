import cv2
import os
import shutil
import mido
import tkinter


def resize_image(image, size=(16, 16)):
    return cv2.resize(image, size, cv2.INTER_LINEAR)


def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def binarize(image):
    _, binary_image = cv2.threshold(
        image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )
    return binary_image


def video_to_image_list(video, target_framerate):
    # Initialize variables
    current_frame = 1
    video_framerate = video.get(5)
    frame_image_list = []

    # Process video frames
    while True:
        ret, frame_image = video.read()
        if ret:
            actual_framerate = int(video_framerate / target_framerate)
            if current_frame % actual_framerate == 0:
                frame_image_afterprocess = binarize(
                    convert_to_grayscale(resize_image(frame_image))
                )
                frame_image_list.append(frame_image_afterprocess)

            current_frame += 1
            cv2.waitKey(0)
        else:
            break
    video.release()
    return frame_image_list


def pnglist_to_midifile(frame_image_list, framerate):
    midifile = mido.MidiFile()
    meta_track = mido.MidiTrack()
    data_track = mido.MidiTrack()

    meta_track.append(mido.MetaMessage("set_tempo", tempo=500000))

    for image in frame_image_list:
        image_binarylist = image.tolist()

        for line in range(len(image_binarylist)):
            image_binarylist_currentline = image_binarylist[line]

            count_column = 0
            for count_column in range(image_binarylist_currentline.count(0)):
                image_binarylist_currentline[image_binarylist_currentline.index(0)] = 1

            count_column = 0
            for count_column in range(image_binarylist[line].count(255)):
                image_binarylist_currentline[
                    image_binarylist_currentline.index(255)
                ] = 0

            image_binarylist[line] = image_binarylist_currentline

        image_sysexlist = [
            16 * image_binarylist[row][col_start + 0]
            + 8 * image_binarylist[row][col_start + 1]
            + 4 * image_binarylist[row][col_start + 2]
            + 2 * image_binarylist[row][col_start + 3]
            + 1 * image_binarylist[row][col_start + 4]
            for col_start in [0, 5, 10]
            for row in range(16)
        ] + [16 * image_binarylist[row][15] for row in range(16)]

        image_sysex_sum = 0
        for ele in range(0, len(image_sysexlist)):
            image_sysex_sum = image_sysex_sum + image_sysexlist[ele]
        image_sysex_checksum = [128 - (17 + image_sysex_sum) % 128]
        if image_sysex_checksum == [128]:
            image_sysex_checksum = [0]

        image_sysexlist_withchecksum = (
            [0x41, 0x10, 0x45, 0x12, 0x10, 0x01, 0x00]
            + image_sysexlist
            + image_sysex_checksum
        )
        data_track.append(
            mido.Message(
                "sysex",
                data=image_sysexlist_withchecksum,
                time=round(48 / (framerate / 10)),
            )
        )
        data_track.append(
            mido.Message(
                "sysex",
                data=[0x41, 0x10, 0x45, 0x12, 0x10, 0x20, 0x00, 0x01, 0x4F],
                time=round(24 / (framerate / 10)),
            )
        )
        data_track.append(
            mido.Message(
                "sysex",
                data=[0x41, 0x10, 0x45, 0x12, 0x10, 0x20, 0x01, 0x01, 0x4E],
                time=round(24 / (framerate / 10)),
            )
        )

    midifile.tracks.append(meta_track)
    midifile.tracks.append(data_track)
    return midifile


def process(videofile, framerate):
    video = cv2.VideoCapture(videofile)
    frame_image_list = video_to_image_list(video, framerate)
    midifile = pnglist_to_midifile(frame_image_list, framerate)
    midifile.save(os.path.splitext(videofile)[0] + ".mid")


process("【東方】Bad Apple!! ＰＶ【影絵】 [BV1xx411c79H].mp4", 30)
