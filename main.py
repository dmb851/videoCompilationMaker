# importing libraries 
import cv2
import numpy as np
import os
import random
import keyboard
import threading
import time
from threading import Timer
from tkinter import *
from tkinter import filedialog


def start_compilation(afile, time1, time2,time3,time4):
    quitVideo = 'false'

    # times for changing song relative to bpm [2bars, 4bars,8bars,16bars]
    bpm_130 = [3.69, 7.38, 14.77]
    bpm_128 = [3.75, 7.5, 15]
    bpm_170 = [2.82, 5.65, 11.29]
    time1=time1.get()
    time2=time2.get()
    time3=time3.get()
    time4=time4.get()

    switch_times = [float(time1),float(time2),float(time3),float(time4)]

    # videos = os.listdir('/Users/dbjer/Desktop/stuff/;p')
    videos = os.listdir(afile)
    print(videos)

    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (1920, 1080))

    total_length = 0

    while total_length < 2000:
        randomVideos = random.sample(videos, len(videos))

        for video in randomVideos:
            print(video)
            # create a random timer to switch to the next video
            timer = switch_times[random.randint(0, 3)]
            print("timer ")
            print(timer)
            total_length += timer

            # Create a VideoCapture object and read from input file
            # file = '/Users/dbjer/Desktop/stuff/;p/' + video
            file = afile + '/' + video
            cap = cv2.VideoCapture(file)

            # create a random position to start the video
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(length)
            safeStart = length-170
            if safeStart < 0:
                continue
            randomPosition = random.randint(0, safeStart)

            cap.set(cv2.CAP_PROP_POS_FRAMES, randomPosition)

            timeout_start = time.time()

            # Check if camera opened successfully
            if (cap.isOpened() == False):
                print("Error opening video  file")

            # Read until video is completed
            while (cap.isOpened()):

                # Capture frame-by-frame
                ret, frame = cap.read()

                if ret == True:
                    # Display the resulting frame
                    cv2.imshow('Frame', frame)

                    # Convert to correct size and Write the frame into the file 'output.avi'
                    resizedFrame = cv2.resize(frame, (1920, 1080), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
                    out.write(resizedFrame)

                    #see if it is time to switch videos
                    if time.time() > timeout_start + timer:
                        break
                    # Press Q on keyboard to  exit
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        quitVideo = 'true'
                        cap.release()
                        out.release()
                        # Closes all the frames
                        cv2.destroyAllWindows()
                        return
                        break
                    if keyboard.is_pressed('e'):
                        break


                # Break the loop
                else:
                    break

            if quitVideo == 'true':
                cap.release()
                out.release()
                # Closes all the frames
                cv2.destroyAllWindows()
                return


            # When everything done, release
            # the video capture object
            cap.release()

    out.release()
    # Closes all the frames
    cv2.destroyAllWindows()


#START GUI

window = Tk()
window.geometry('500x500')
window.resizable(width=False, height=False)

window.title("Compilation Maker")

lbl = Label(window, text="Choose a folder with your videos in it")
lbl.place(x=20, y=25)

videopath = StringVar()
videolbl = Label(window, textvariable=videopath)
videolbl.place(x=250,y=50)


def file_clicked():
    file = filedialog.askdirectory()
    print(file)
    videopath.set(file)
    # start_compilation(file, atime1, atime2, atime3, atime4)


def start_clicked():
    start_compilation(videopath.get(), atime1, atime2, atime3, atime4)

btn = Button(window, text="Choose Folder", command=file_clicked)
btn.place(x=250,y=25)



# IMPLEMENT BPM SYNC HERE
# bpmlabel = Label(window, text="Choose a Bpm")
# bpmlabel.grid(column=0, row=2)
# spin = Spinbox(window, from_=0, to=100, width=5)
# spin.grid(column=0,row=3)
# END BPM SYNC


timeslbl = Label(window, text="Pick times for scene/video changes")
timeslbl.place(x=20,y=75)
#times for scene changes
v1 = StringVar(window, value='0')
v2 = StringVar(window, value='0')
v3 = StringVar(window, value='0')
v4 = StringVar(window, value='0')

atime1 = Entry(window, textvariable=v1,width=7)
atime1.place(x=250,y=75)

atime2 = Entry(window,textvariable=v2,width=7)
atime2.place(x=300,y=75)

atime3 = Entry(window,textvariable=v3,width=7)
atime3.place(x=350,y=75)

atime4 = Entry(window,textvariable=v4,width=7)
atime4.place(x=400,y=75)


# END GUI
#start gui again
startbtn = Button(window, text="START", command=start_clicked)
startbtn.place(x=200,y=150)

dashes1 = Label(window, text="-------------------------------------")
dashes2 = Label(window, text="-------------------------------------")
dashes1.place(x=150,y=300)
dashes2.place(x=150,y=450)


lbl1 = Label(window, text="Instructions When Video Is Playing:")
lbl1.place(x=150,y=350)

lbl2 = Label(window, text="Press q to quit")
lbl2.place(x=150,y=375)

lbl3 = Label(window, text="Press e to skip to next video")
lbl3.place(x=150,y=400)


window.mainloop()

#end gui