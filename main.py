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
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary_image


def image_to_list(image):
    return image.tolist()


def video_to_pnglist(video, target_framerate):
    # Initialize variables
    current_frame = 1
    video_framerate = video.get(5)

    # Create cache folder
    try:
        if not os.path.exists(".cache"):
            os.makedirs(".cache")
    except OSError:
        print ("Error: Couldn't create cache folder.")
    
    # Process video frames
    while True:
        ret, frame_image = video.read()
        if ret:
            actual_framerate = int(video_framerate / target_framerate)
            if(current_frame % actual_framerate == 0):
                frame_image_afterprocess = binarize(
                    convert_to_grayscale(
                        resize_image(frame_image)
                    )
                )
                cv2.imwrite(
                    ".cache/" + str("{:0>8.0f}".format(current_frame)) + ".png", 
                    frame_image_afterprocess
                )
                
            current_frame += 1
            cv2.waitKey(0)
        else:
            break
    video.release()


def pnglist_to_midifile(videofile, framerate):
    imagelist = os.listdir(".cache")
    midifile = mido.MidiFile()
    meta_track = mido.MidiTrack()
    data_track = mido.MidiTrack()
    
    meta_track.append(mido.MetaMessage("set_tempo", tempo = 500000))

    for image_name in imagelist:
        image = cv2.imread(".cache/" + image_name)
        image_binarylist = image.tolist()

        for line in range(len(image_binarylist)):
            image_binarylist_currentline = image_binarylist[line]

            count_column = 0
            for count_column in range(image_binarylist_currentline.count([0, 0, 0])):
                image_binarylist_currentline[image_binarylist_currentline.index([0, 0, 0])] = 1
                count_column += 1

            count_column = 0
            for count_column in range(image_binarylist[line].count([255, 255, 255])):
                image_binarylist_currentline[image_binarylist_currentline.index([255, 255, 255])] = 0
                count_column += 1

            image_binarylist[line] = image_binarylist_currentline
            line += 1

        image_sysexlist = [16 * image_binarylist[0 ][0 ] +
                               8 * image_binarylist[0 ][1 ] +
                               4 * image_binarylist[0 ][2 ] +
                               2 * image_binarylist[0 ][3 ] +
                               1 * image_binarylist[0 ][4 ],
                              16 * image_binarylist[1 ][0 ] +
                               8 * image_binarylist[1 ][1 ] +
                               4 * image_binarylist[1 ][2 ] +
                               2 * image_binarylist[1 ][3 ] +
                               1 * image_binarylist[1 ][4 ],
                              16 * image_binarylist[2 ][0 ] +
                               8 * image_binarylist[2 ][1 ] +
                               4 * image_binarylist[2 ][2 ] +
                               2 * image_binarylist[2 ][3 ] +
                               1 * image_binarylist[2 ][4 ],
                              16 * image_binarylist[3 ][0 ] +
                               8 * image_binarylist[3 ][1 ] +
                               4 * image_binarylist[3 ][2 ] +
                               2 * image_binarylist[3 ][3 ] +
                               1 * image_binarylist[3 ][4 ],
                              16 * image_binarylist[4 ][0 ] +
                               8 * image_binarylist[4 ][1 ] +
                               4 * image_binarylist[4 ][2 ] +
                               2 * image_binarylist[4 ][3 ] +
                               1 * image_binarylist[4 ][4 ],
                              16 * image_binarylist[5 ][0 ] +
                               8 * image_binarylist[5 ][1 ] +
                               4 * image_binarylist[5 ][2 ] +
                               2 * image_binarylist[5 ][3 ] +
                               1 * image_binarylist[5 ][4 ],
                              16 * image_binarylist[6 ][0 ] +
                               8 * image_binarylist[6 ][1 ] +
                               4 * image_binarylist[6 ][2 ] +
                               2 * image_binarylist[6 ][3 ] +
                               1 * image_binarylist[6 ][4 ],
                              16 * image_binarylist[7 ][0 ] +
                               8 * image_binarylist[7 ][1 ] +
                               4 * image_binarylist[7 ][2 ] +
                               2 * image_binarylist[7 ][3 ] +
                               1 * image_binarylist[7 ][4 ],
                              16 * image_binarylist[8 ][0 ] +
                               8 * image_binarylist[8 ][1 ] +
                               4 * image_binarylist[8 ][2 ] +
                               2 * image_binarylist[8 ][3 ] +
                               1 * image_binarylist[8 ][4 ],
                              16 * image_binarylist[9 ][0 ] +
                               8 * image_binarylist[9 ][1 ] +
                               4 * image_binarylist[9 ][2 ] +
                               2 * image_binarylist[9 ][3 ] +
                               1 * image_binarylist[9 ][4 ],
                              16 * image_binarylist[10][0 ] +
                               8 * image_binarylist[10][1 ] +
                               4 * image_binarylist[10][2 ] +
                               2 * image_binarylist[10][3 ] +
                               1 * image_binarylist[10][4 ],
                              16 * image_binarylist[11][0 ] +
                               8 * image_binarylist[11][1 ] +
                               4 * image_binarylist[11][2 ] +
                               2 * image_binarylist[11][3 ] +
                               1 * image_binarylist[11][4 ],
                              16 * image_binarylist[12][0 ] +
                               8 * image_binarylist[12][1 ] +
                               4 * image_binarylist[12][2 ] +
                               2 * image_binarylist[12][3 ] +
                               1 * image_binarylist[12][4 ],
                              16 * image_binarylist[13][0 ] +
                               8 * image_binarylist[13][1 ] +
                               4 * image_binarylist[13][2 ] +
                               2 * image_binarylist[13][3 ] +
                               1 * image_binarylist[13][4 ],
                              16 * image_binarylist[14][0 ] +
                               8 * image_binarylist[14][1 ] +
                               4 * image_binarylist[14][2 ] +
                               2 * image_binarylist[14][3 ] +
                               1 * image_binarylist[14][4 ],
                              16 * image_binarylist[15][0 ] +
                               8 * image_binarylist[15][1 ] +
                               4 * image_binarylist[15][2 ] +
                               2 * image_binarylist[15][3 ] +
                               1 * image_binarylist[15][4 ],

                              16 * image_binarylist[0 ][5 ] +
                               8 * image_binarylist[0 ][6 ] +
                               4 * image_binarylist[0 ][7 ] +
                               2 * image_binarylist[0 ][8 ] +
                               1 * image_binarylist[0 ][9 ],
                              16 * image_binarylist[1 ][5 ] +
                               8 * image_binarylist[1 ][6 ] +
                               4 * image_binarylist[1 ][7 ] +
                               2 * image_binarylist[1 ][8 ] +
                               1 * image_binarylist[1 ][9 ],
                              16 * image_binarylist[2 ][5 ] +
                               8 * image_binarylist[2 ][6 ] +
                               4 * image_binarylist[2 ][7 ] +
                               2 * image_binarylist[2 ][8 ] +
                               1 * image_binarylist[2 ][9 ],
                              16 * image_binarylist[3 ][5 ] +
                               8 * image_binarylist[3 ][6 ] +
                               4 * image_binarylist[3 ][7 ] +
                               2 * image_binarylist[3 ][8 ] +
                               1 * image_binarylist[3 ][9 ],
                              16 * image_binarylist[4 ][5 ] +
                               8 * image_binarylist[4 ][6 ] +
                               4 * image_binarylist[4 ][7 ] +
                               2 * image_binarylist[4 ][8 ] +
                               1 * image_binarylist[4 ][9 ],
                              16 * image_binarylist[5 ][5 ] +
                               8 * image_binarylist[5 ][6 ] +
                               4 * image_binarylist[5 ][7 ] +
                               2 * image_binarylist[5 ][8 ] +
                               1 * image_binarylist[5 ][9 ],
                              16 * image_binarylist[6 ][5 ] +
                               8 * image_binarylist[6 ][6 ] +
                               4 * image_binarylist[6 ][7 ] +
                               2 * image_binarylist[6 ][8 ] +
                               1 * image_binarylist[6 ][9 ],
                              16 * image_binarylist[7 ][5 ] +
                               8 * image_binarylist[7 ][6 ] +
                               4 * image_binarylist[7 ][7 ] +
                               2 * image_binarylist[7 ][8 ] +
                               1 * image_binarylist[7 ][9 ],
                              16 * image_binarylist[8 ][5 ] +
                               8 * image_binarylist[8 ][6 ] +
                               4 * image_binarylist[8 ][7 ] +
                               2 * image_binarylist[8 ][8 ] +
                               1 * image_binarylist[8 ][9 ],
                              16 * image_binarylist[9 ][5 ] +
                               8 * image_binarylist[9 ][6 ] +
                               4 * image_binarylist[9 ][7 ] +
                               2 * image_binarylist[9 ][8 ] +
                               1 * image_binarylist[9 ][9 ],
                              16 * image_binarylist[10][5 ] +
                               8 * image_binarylist[10][6 ] +
                               4 * image_binarylist[10][7 ] +
                               2 * image_binarylist[10][8 ] +
                               1 * image_binarylist[10][9 ],
                              16 * image_binarylist[11][5 ] +
                               8 * image_binarylist[11][6 ] +
                               4 * image_binarylist[11][7 ] +
                               2 * image_binarylist[11][8 ] +
                               1 * image_binarylist[11][9 ],
                              16 * image_binarylist[12][5 ] +
                               8 * image_binarylist[12][6 ] +
                               4 * image_binarylist[12][7 ] +
                               2 * image_binarylist[12][8 ] +
                               1 * image_binarylist[12][9 ],
                              16 * image_binarylist[13][5 ] +
                               8 * image_binarylist[13][6 ] +
                               4 * image_binarylist[13][7 ] +
                               2 * image_binarylist[13][8 ] +
                               1 * image_binarylist[13][9 ],
                              16 * image_binarylist[14][5 ] +
                               8 * image_binarylist[14][6 ] +
                               4 * image_binarylist[14][7 ] +
                               2 * image_binarylist[14][8 ] +
                               1 * image_binarylist[14][9 ],
                              16 * image_binarylist[15][5 ] +
                               8 * image_binarylist[15][6 ] +
                               4 * image_binarylist[15][7 ] +
                               2 * image_binarylist[15][8 ] +
                               1 * image_binarylist[15][9 ],

                              16 * image_binarylist[0 ][10] +
                               8 * image_binarylist[0 ][11] +
                               4 * image_binarylist[0 ][12] +
                               2 * image_binarylist[0 ][13] +
                               1 * image_binarylist[0 ][14],
                              16 * image_binarylist[1 ][10] +
                               8 * image_binarylist[1 ][11] +
                               4 * image_binarylist[1 ][12] +
                               2 * image_binarylist[1 ][13] +
                               1 * image_binarylist[1 ][14],
                              16 * image_binarylist[2 ][10] +
                               8 * image_binarylist[2 ][11] +
                               4 * image_binarylist[2 ][12] +
                               2 * image_binarylist[2 ][13] +
                               1 * image_binarylist[2 ][14],
                              16 * image_binarylist[3 ][10] +
                               8 * image_binarylist[3 ][11] +
                               4 * image_binarylist[3 ][12] +
                               2 * image_binarylist[3 ][13] +
                               1 * image_binarylist[3 ][14],
                              16 * image_binarylist[4 ][10] +
                               8 * image_binarylist[4 ][11] +
                               4 * image_binarylist[4 ][12] +
                               2 * image_binarylist[4 ][13] +
                               1 * image_binarylist[4 ][14],
                              16 * image_binarylist[5 ][10] +
                               8 * image_binarylist[5 ][11] +
                               4 * image_binarylist[5 ][12] +
                               2 * image_binarylist[5 ][13] +
                               1 * image_binarylist[5 ][14],
                              16 * image_binarylist[6 ][10] +
                               8 * image_binarylist[6 ][11] +
                               4 * image_binarylist[6 ][12] +
                               2 * image_binarylist[6 ][13] +
                               1 * image_binarylist[6 ][14],
                              16 * image_binarylist[7 ][10] +
                               8 * image_binarylist[7 ][11] +
                               4 * image_binarylist[7 ][12] +
                               2 * image_binarylist[7 ][13] +
                               1 * image_binarylist[7 ][14],
                              16 * image_binarylist[8 ][10] +
                               8 * image_binarylist[8 ][11] +
                               4 * image_binarylist[8 ][12] +
                               2 * image_binarylist[8 ][13] +
                               1 * image_binarylist[8 ][14],
                              16 * image_binarylist[9 ][10] +
                               8 * image_binarylist[9 ][11] +
                               4 * image_binarylist[9 ][12] +
                               2 * image_binarylist[9 ][13] +
                               1 * image_binarylist[9 ][14],
                              16 * image_binarylist[10][10] +
                               8 * image_binarylist[10][11] +
                               4 * image_binarylist[10][12] +
                               2 * image_binarylist[10][13] +
                               1 * image_binarylist[10][14],
                              16 * image_binarylist[11][10] +
                               8 * image_binarylist[11][11] +
                               4 * image_binarylist[11][12] +
                               2 * image_binarylist[11][13] +
                               1 * image_binarylist[11][14],
                              16 * image_binarylist[12][10] +
                               8 * image_binarylist[12][11] +
                               4 * image_binarylist[12][12] +
                               2 * image_binarylist[12][13] +
                               1 * image_binarylist[12][14],
                              16 * image_binarylist[13][10] +
                               8 * image_binarylist[13][11] +
                               4 * image_binarylist[13][12] +
                               2 * image_binarylist[13][13] +
                               1 * image_binarylist[13][14],
                              16 * image_binarylist[14][10] +
                               8 * image_binarylist[14][11] +
                               4 * image_binarylist[14][12] +
                               2 * image_binarylist[14][13] +
                               1 * image_binarylist[14][14],
                              16 * image_binarylist[15][10] +
                               8 * image_binarylist[15][11] +
                               4 * image_binarylist[15][12] +
                               2 * image_binarylist[15][13] +
                               1 * image_binarylist[15][14],

                              16 * image_binarylist[0 ][15],
                              16 * image_binarylist[1 ][15],
                              16 * image_binarylist[2 ][15],
                              16 * image_binarylist[3 ][15],
                              16 * image_binarylist[4 ][15],
                              16 * image_binarylist[5 ][15],
                              16 * image_binarylist[6 ][15],
                              16 * image_binarylist[7 ][15],
                              16 * image_binarylist[8 ][15],
                              16 * image_binarylist[9 ][15],
                              16 * image_binarylist[10][15],
                              16 * image_binarylist[11][15],
                              16 * image_binarylist[12][15],
                              16 * image_binarylist[13][15],
                              16 * image_binarylist[14][15],
                              16 * image_binarylist[15][15]]
        image_sysex_sum = 0
        for ele in range(0, len(image_sysexlist)):
            image_sysex_sum = image_sysex_sum + image_sysexlist[ele]
        image_sysex_checksum = [128 - (17 + image_sysex_sum) % 128]
        if image_sysex_checksum == [128]:
            image_sysex_checksum = [0]
        image_sysexlist_withchecksum = [0x41, 0x10, 0x45, 0x12, 0x10, 0x01, 0x00] + image_sysexlist + image_sysex_checksum
        print(image_sysexlist_withchecksum)
        data_track.append(mido.Message("sysex", data=image_sysexlist_withchecksum, time=round(48 / (framerate / 10))))
        data_track.append(mido.Message("sysex", data=[0x41, 0x10, 0x45, 0x12, 0x10, 0x20, 0x00, 0x01, 0x4f], time=round(24 / (framerate / 10))))
        data_track.append(mido.Message("sysex", data=[0x41, 0x10, 0x45, 0x12, 0x10, 0x20, 0x01, 0x01, 0x4e], time=round(24 / (framerate / 10))))

    midifile.tracks.append(meta_track)
    midifile.tracks.append(data_track)
    midifile.save(os.path.splitext(videofile)[0] + ".mid")


def process(videofile, framerate):
    if os.path.exists(".cache"):
        shutil.rmtree(".cache")

    video = cv2.VideoCapture(videofile)
    video_to_pnglist(video, framerate)
    pnglist_to_midifile(videofile, framerate)
    shutil.rmtree(".cache")


process("【東方】Bad Apple!! ＰＶ【影絵】.mp4", 30)
'''
mainwindow = tkinter.Tk()
mainwindow.title("Video Canvas")
mainwindow.geometry("480x320")
mainwindow.iconbitmap("resources/16x16.ico")
defaultfont = ("等线", 10, "normal")
tkinter.LabelFrame(mainwindow, text="文件选择...", font=defaultfont, width=470, height=90).place(x=5, y=0)
videofileentry = tkinter.Entry(mainwindow, font=defaultfont, width=65).place(x=10, y=20)
button = tkinter.Button(mainwindow, text="浏览...", command=NotImplemented).place(x=425, y=50)

mainwindow.mainloop()
'''