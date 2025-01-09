import cv2
import os
import shutil
import mido
import tkinter


def ConvertVideoToPngList(videofile, targetframerate):
    currentframe = 1
    video = cv2.VideoCapture(videofile)
    videoframerate = video.get(5)

    try:
        if not os.path.exists(".cache"):
            os.makedirs(".cache")
    except OSError:
        print ("Error: Couldn't create cache folder.")

    while True:
        ret, frameimage = video.read()
        if ret:
            actualframerate = int(videoframerate / targetframerate)
            if(currentframe % actualframerate == 0):
                ret, frameimage = cv2.threshold(cv2.cvtColor(cv2.resize(frameimage, (16, 16), cv2.INTER_LINEAR), cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                cv2.imwrite(".cache/" + str("{:0>8.0f}".format(currentframe)) + ".png", frameimage)
            currentframe += 1
            cv2.waitKey(0)
        else:
            break
    video.release()


def PngListToMIDIFile(videofile, framerate):
    imagelist = os.listdir(".cache")
    outputmidifile = mido.MidiFile()
    metatrack = mido.MidiTrack()
    datatrack = mido.MidiTrack()
    
    metatrack.append(mido.MetaMessage("set_tempo", tempo = 500000))

    for imagename in imagelist:
        image = cv2.imread(".cache/" + imagename)
        imagebinarydatalist = image.tolist()

        for line in range(len(imagebinarydatalist)):
            imagebinarydatalistline = imagebinarydatalist[line]

            countcolumn = 0
            for countcolumn in range(imagebinarydatalistline.count([0, 0, 0])):
                imagebinarydatalistline[imagebinarydatalistline.index([0, 0, 0])] = 1
                countcolumn += 1

            countcolumn = 0
            for countcolumn in range(imagebinarydatalist[line].count([255, 255, 255])):
                imagebinarydatalistline[imagebinarydatalistline.index([255, 255, 255])] = 0
                countcolumn += 1

            imagebinarydatalist[line] = imagebinarydatalistline
        line += 1

        imagesysexdatalist = [16 * imagebinarydatalist[0 ][0 ] +
                               8 * imagebinarydatalist[0 ][1 ] +
                               4 * imagebinarydatalist[0 ][2 ] +
                               2 * imagebinarydatalist[0 ][3 ] +
                               1 * imagebinarydatalist[0 ][4 ],
                              16 * imagebinarydatalist[1 ][0 ] +
                               8 * imagebinarydatalist[1 ][1 ] +
                               4 * imagebinarydatalist[1 ][2 ] +
                               2 * imagebinarydatalist[1 ][3 ] +
                               1 * imagebinarydatalist[1 ][4 ],
                              16 * imagebinarydatalist[2 ][0 ] +
                               8 * imagebinarydatalist[2 ][1 ] +
                               4 * imagebinarydatalist[2 ][2 ] +
                               2 * imagebinarydatalist[2 ][3 ] +
                               1 * imagebinarydatalist[2 ][4 ],
                              16 * imagebinarydatalist[3 ][0 ] +
                               8 * imagebinarydatalist[3 ][1 ] +
                               4 * imagebinarydatalist[3 ][2 ] +
                               2 * imagebinarydatalist[3 ][3 ] +
                               1 * imagebinarydatalist[3 ][4 ],
                              16 * imagebinarydatalist[4 ][0 ] +
                               8 * imagebinarydatalist[4 ][1 ] +
                               4 * imagebinarydatalist[4 ][2 ] +
                               2 * imagebinarydatalist[4 ][3 ] +
                               1 * imagebinarydatalist[4 ][4 ],
                              16 * imagebinarydatalist[5 ][0 ] +
                               8 * imagebinarydatalist[5 ][1 ] +
                               4 * imagebinarydatalist[5 ][2 ] +
                               2 * imagebinarydatalist[5 ][3 ] +
                               1 * imagebinarydatalist[5 ][4 ],
                              16 * imagebinarydatalist[6 ][0 ] +
                               8 * imagebinarydatalist[6 ][1 ] +
                               4 * imagebinarydatalist[6 ][2 ] +
                               2 * imagebinarydatalist[6 ][3 ] +
                               1 * imagebinarydatalist[6 ][4 ],
                              16 * imagebinarydatalist[7 ][0 ] +
                               8 * imagebinarydatalist[7 ][1 ] +
                               4 * imagebinarydatalist[7 ][2 ] +
                               2 * imagebinarydatalist[7 ][3 ] +
                               1 * imagebinarydatalist[7 ][4 ],
                              16 * imagebinarydatalist[8 ][0 ] +
                               8 * imagebinarydatalist[8 ][1 ] +
                               4 * imagebinarydatalist[8 ][2 ] +
                               2 * imagebinarydatalist[8 ][3 ] +
                               1 * imagebinarydatalist[8 ][4 ],
                              16 * imagebinarydatalist[9 ][0 ] +
                               8 * imagebinarydatalist[9 ][1 ] +
                               4 * imagebinarydatalist[9 ][2 ] +
                               2 * imagebinarydatalist[9 ][3 ] +
                               1 * imagebinarydatalist[9 ][4 ],
                              16 * imagebinarydatalist[10][0 ] +
                               8 * imagebinarydatalist[10][1 ] +
                               4 * imagebinarydatalist[10][2 ] +
                               2 * imagebinarydatalist[10][3 ] +
                               1 * imagebinarydatalist[10][4 ],
                              16 * imagebinarydatalist[11][0 ] +
                               8 * imagebinarydatalist[11][1 ] +
                               4 * imagebinarydatalist[11][2 ] +
                               2 * imagebinarydatalist[11][3 ] +
                               1 * imagebinarydatalist[11][4 ],
                              16 * imagebinarydatalist[12][0 ] +
                               8 * imagebinarydatalist[12][1 ] +
                               4 * imagebinarydatalist[12][2 ] +
                               2 * imagebinarydatalist[12][3 ] +
                               1 * imagebinarydatalist[12][4 ],
                              16 * imagebinarydatalist[13][0 ] +
                               8 * imagebinarydatalist[13][1 ] +
                               4 * imagebinarydatalist[13][2 ] +
                               2 * imagebinarydatalist[13][3 ] +
                               1 * imagebinarydatalist[13][4 ],
                              16 * imagebinarydatalist[14][0 ] +
                               8 * imagebinarydatalist[14][1 ] +
                               4 * imagebinarydatalist[14][2 ] +
                               2 * imagebinarydatalist[14][3 ] +
                               1 * imagebinarydatalist[14][4 ],
                              16 * imagebinarydatalist[15][0 ] +
                               8 * imagebinarydatalist[15][1 ] +
                               4 * imagebinarydatalist[15][2 ] +
                               2 * imagebinarydatalist[15][3 ] +
                               1 * imagebinarydatalist[15][4 ],

                              16 * imagebinarydatalist[0 ][5 ] +
                               8 * imagebinarydatalist[0 ][6 ] +
                               4 * imagebinarydatalist[0 ][7 ] +
                               2 * imagebinarydatalist[0 ][8 ] +
                               1 * imagebinarydatalist[0 ][9 ],
                              16 * imagebinarydatalist[1 ][5 ] +
                               8 * imagebinarydatalist[1 ][6 ] +
                               4 * imagebinarydatalist[1 ][7 ] +
                               2 * imagebinarydatalist[1 ][8 ] +
                               1 * imagebinarydatalist[1 ][9 ],
                              16 * imagebinarydatalist[2 ][5 ] +
                               8 * imagebinarydatalist[2 ][6 ] +
                               4 * imagebinarydatalist[2 ][7 ] +
                               2 * imagebinarydatalist[2 ][8 ] +
                               1 * imagebinarydatalist[2 ][9 ],
                              16 * imagebinarydatalist[3 ][5 ] +
                               8 * imagebinarydatalist[3 ][6 ] +
                               4 * imagebinarydatalist[3 ][7 ] +
                               2 * imagebinarydatalist[3 ][8 ] +
                               1 * imagebinarydatalist[3 ][9 ],
                              16 * imagebinarydatalist[4 ][5 ] +
                               8 * imagebinarydatalist[4 ][6 ] +
                               4 * imagebinarydatalist[4 ][7 ] +
                               2 * imagebinarydatalist[4 ][8 ] +
                               1 * imagebinarydatalist[4 ][9 ],
                              16 * imagebinarydatalist[5 ][5 ] +
                               8 * imagebinarydatalist[5 ][6 ] +
                               4 * imagebinarydatalist[5 ][7 ] +
                               2 * imagebinarydatalist[5 ][8 ] +
                               1 * imagebinarydatalist[5 ][9 ],
                              16 * imagebinarydatalist[6 ][5 ] +
                               8 * imagebinarydatalist[6 ][6 ] +
                               4 * imagebinarydatalist[6 ][7 ] +
                               2 * imagebinarydatalist[6 ][8 ] +
                               1 * imagebinarydatalist[6 ][9 ],
                              16 * imagebinarydatalist[7 ][5 ] +
                               8 * imagebinarydatalist[7 ][6 ] +
                               4 * imagebinarydatalist[7 ][7 ] +
                               2 * imagebinarydatalist[7 ][8 ] +
                               1 * imagebinarydatalist[7 ][9 ],
                              16 * imagebinarydatalist[8 ][5 ] +
                               8 * imagebinarydatalist[8 ][6 ] +
                               4 * imagebinarydatalist[8 ][7 ] +
                               2 * imagebinarydatalist[8 ][8 ] +
                               1 * imagebinarydatalist[8 ][9 ],
                              16 * imagebinarydatalist[9 ][5 ] +
                               8 * imagebinarydatalist[9 ][6 ] +
                               4 * imagebinarydatalist[9 ][7 ] +
                               2 * imagebinarydatalist[9 ][8 ] +
                               1 * imagebinarydatalist[9 ][9 ],
                              16 * imagebinarydatalist[10][5 ] +
                               8 * imagebinarydatalist[10][6 ] +
                               4 * imagebinarydatalist[10][7 ] +
                               2 * imagebinarydatalist[10][8 ] +
                               1 * imagebinarydatalist[10][9 ],
                              16 * imagebinarydatalist[11][5 ] +
                               8 * imagebinarydatalist[11][6 ] +
                               4 * imagebinarydatalist[11][7 ] +
                               2 * imagebinarydatalist[11][8 ] +
                               1 * imagebinarydatalist[11][9 ],
                              16 * imagebinarydatalist[12][5 ] +
                               8 * imagebinarydatalist[12][6 ] +
                               4 * imagebinarydatalist[12][7 ] +
                               2 * imagebinarydatalist[12][8 ] +
                               1 * imagebinarydatalist[12][9 ],
                              16 * imagebinarydatalist[13][5 ] +
                               8 * imagebinarydatalist[13][6 ] +
                               4 * imagebinarydatalist[13][7 ] +
                               2 * imagebinarydatalist[13][8 ] +
                               1 * imagebinarydatalist[13][9 ],
                              16 * imagebinarydatalist[14][5 ] +
                               8 * imagebinarydatalist[14][6 ] +
                               4 * imagebinarydatalist[14][7 ] +
                               2 * imagebinarydatalist[14][8 ] +
                               1 * imagebinarydatalist[14][9 ],
                              16 * imagebinarydatalist[15][5 ] +
                               8 * imagebinarydatalist[15][6 ] +
                               4 * imagebinarydatalist[15][7 ] +
                               2 * imagebinarydatalist[15][8 ] +
                               1 * imagebinarydatalist[15][9 ],

                              16 * imagebinarydatalist[0 ][10] +
                               8 * imagebinarydatalist[0 ][11] +
                               4 * imagebinarydatalist[0 ][12] +
                               2 * imagebinarydatalist[0 ][13] +
                               1 * imagebinarydatalist[0 ][14],
                              16 * imagebinarydatalist[1 ][10] +
                               8 * imagebinarydatalist[1 ][11] +
                               4 * imagebinarydatalist[1 ][12] +
                               2 * imagebinarydatalist[1 ][13] +
                               1 * imagebinarydatalist[1 ][14],
                              16 * imagebinarydatalist[2 ][10] +
                               8 * imagebinarydatalist[2 ][11] +
                               4 * imagebinarydatalist[2 ][12] +
                               2 * imagebinarydatalist[2 ][13] +
                               1 * imagebinarydatalist[2 ][14],
                              16 * imagebinarydatalist[3 ][10] +
                               8 * imagebinarydatalist[3 ][11] +
                               4 * imagebinarydatalist[3 ][12] +
                               2 * imagebinarydatalist[3 ][13] +
                               1 * imagebinarydatalist[3 ][14],
                              16 * imagebinarydatalist[4 ][10] +
                               8 * imagebinarydatalist[4 ][11] +
                               4 * imagebinarydatalist[4 ][12] +
                               2 * imagebinarydatalist[4 ][13] +
                               1 * imagebinarydatalist[4 ][14],
                              16 * imagebinarydatalist[5 ][10] +
                               8 * imagebinarydatalist[5 ][11] +
                               4 * imagebinarydatalist[5 ][12] +
                               2 * imagebinarydatalist[5 ][13] +
                               1 * imagebinarydatalist[5 ][14],
                              16 * imagebinarydatalist[6 ][10] +
                               8 * imagebinarydatalist[6 ][11] +
                               4 * imagebinarydatalist[6 ][12] +
                               2 * imagebinarydatalist[6 ][13] +
                               1 * imagebinarydatalist[6 ][14],
                              16 * imagebinarydatalist[7 ][10] +
                               8 * imagebinarydatalist[7 ][11] +
                               4 * imagebinarydatalist[7 ][12] +
                               2 * imagebinarydatalist[7 ][13] +
                               1 * imagebinarydatalist[7 ][14],
                              16 * imagebinarydatalist[8 ][10] +
                               8 * imagebinarydatalist[8 ][11] +
                               4 * imagebinarydatalist[8 ][12] +
                               2 * imagebinarydatalist[8 ][13] +
                               1 * imagebinarydatalist[8 ][14],
                              16 * imagebinarydatalist[9 ][10] +
                               8 * imagebinarydatalist[9 ][11] +
                               4 * imagebinarydatalist[9 ][12] +
                               2 * imagebinarydatalist[9 ][13] +
                               1 * imagebinarydatalist[9 ][14],
                              16 * imagebinarydatalist[10][10] +
                               8 * imagebinarydatalist[10][11] +
                               4 * imagebinarydatalist[10][12] +
                               2 * imagebinarydatalist[10][13] +
                               1 * imagebinarydatalist[10][14],
                              16 * imagebinarydatalist[11][10] +
                               8 * imagebinarydatalist[11][11] +
                               4 * imagebinarydatalist[11][12] +
                               2 * imagebinarydatalist[11][13] +
                               1 * imagebinarydatalist[11][14],
                              16 * imagebinarydatalist[12][10] +
                               8 * imagebinarydatalist[12][11] +
                               4 * imagebinarydatalist[12][12] +
                               2 * imagebinarydatalist[12][13] +
                               1 * imagebinarydatalist[12][14],
                              16 * imagebinarydatalist[13][10] +
                               8 * imagebinarydatalist[13][11] +
                               4 * imagebinarydatalist[13][12] +
                               2 * imagebinarydatalist[13][13] +
                               1 * imagebinarydatalist[13][14],
                              16 * imagebinarydatalist[14][10] +
                               8 * imagebinarydatalist[14][11] +
                               4 * imagebinarydatalist[14][12] +
                               2 * imagebinarydatalist[14][13] +
                               1 * imagebinarydatalist[14][14],
                              16 * imagebinarydatalist[15][10] +
                               8 * imagebinarydatalist[15][11] +
                               4 * imagebinarydatalist[15][12] +
                               2 * imagebinarydatalist[15][13] +
                               1 * imagebinarydatalist[15][14],

                              16 * imagebinarydatalist[0 ][15],
                              16 * imagebinarydatalist[1 ][15],
                              16 * imagebinarydatalist[2 ][15],
                              16 * imagebinarydatalist[3 ][15],
                              16 * imagebinarydatalist[4 ][15],
                              16 * imagebinarydatalist[5 ][15],
                              16 * imagebinarydatalist[6 ][15],
                              16 * imagebinarydatalist[7 ][15],
                              16 * imagebinarydatalist[8 ][15],
                              16 * imagebinarydatalist[9 ][15],
                              16 * imagebinarydatalist[10][15],
                              16 * imagebinarydatalist[11][15],
                              16 * imagebinarydatalist[12][15],
                              16 * imagebinarydatalist[13][15],
                              16 * imagebinarydatalist[14][15],
                              16 * imagebinarydatalist[15][15]]
        imagesysexdatasum = 0
        for ele in range(0, len(imagesysexdatalist)):
            imagesysexdatasum = imagesysexdatasum + imagesysexdatalist[ele]
        imagesysexdatachecksum = [128 - (17 + imagesysexdatasum) % 128]
        if imagesysexdatachecksum == [128]:
            imagesysexdatachecksum = [0]
        imagesysexdatalistwithchecksum = [0x41, 0x10, 0x45, 0x12, 0x10, 0x01, 0x00] + imagesysexdatalist + imagesysexdatachecksum
        print(imagesysexdatalistwithchecksum)
        datatrack.append(mido.Message("sysex", data=imagesysexdatalistwithchecksum, time=round(48 / (framerate / 10))))
        datatrack.append(mido.Message("sysex", data=[0x41, 0x10, 0x45, 0x12, 0x10, 0x20, 0x00, 0x01, 0x4f], time=round(24 / (framerate / 10))))
        datatrack.append(mido.Message("sysex", data=[0x41, 0x10, 0x45, 0x12, 0x10, 0x20, 0x01, 0x01, 0x4e], time=round(24 / (framerate / 10))))

    outputmidifile.tracks.append(metatrack)
    outputmidifile.tracks.append(datatrack)
    outputmidifile.save(os.path.splitext(videofile)[0] + ".mid")


def Process(videofile, framerate):
    if os.path.exists(".cache"):
        shutil.rmtree(".cache")

    ConvertVideoToPngList(videofile, framerate)
    PngListToMIDIFile(videofile, framerate)
    shutil.rmtree(".cache")


Process("【東方】Bad Apple!! ＰＶ【影絵】.mp4", 30)
'''
mainwindow = tkinter.Tk()
mainwindow.title("Video Canvas")
mainwindow.geometry("480x320")
mainwindow.iconbitmap("resources/16x16.ico")
defaultfont = ("等线", 10, "normal")
tkinter.LabelFrame(mainwindow, text="文件选择...", font=defaultfont, width=470, height=90).place(x=5, y=0)
videofileentry = tkinter.Entry(mainwindow, font=defaultfont, width=65).place(x=10, y=20)
button = tkinter.Button(mainwindow, text="浏览...", command=).place(x=425, y=50)

mainwindow.mainloop()
'''
