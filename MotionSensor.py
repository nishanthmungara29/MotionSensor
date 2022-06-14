#library for computer vision to read images and videos their manipulation etc..
import cv2
#for manipulation of images like resizing
import imutils
import threading
#module to allow to play a sound on trigger
import winsound

#0 for 1st camera 
#1 for 2nd camera etc....
#capture frames from camera into cap object
#cv2.CAP_DSHOW helps resolve camera initialization issues in windows
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
#setting resolution of captured video frames
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)


#_ refers to one of the return values from cap.read which is a boolean indicating if frame was read succesfully
#statrt_frame captures frame
_,start_frame=cap.read()
#maintaiing original aspect ratio set frame to 500 pixel width
start_frame=imutils.resize(start_frame,width=500)
#changing frame color from blue green red to grayscale
start_frame=cv2.cvtColor(start_frame,cv2.COLOR_BGR2GRAY)
#smoothening image
#(21,21) is amount of blurring
#0 for no deviation
start_frame=cv2.GaussianBlur(start_frame,(21,21),0)

alarm=False
alarm_mode=False
#alarm_counter checks how long after movement alarm must be signaled
alarm_counter=0

def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("ALARM")
        #2500 is frequency
        #1000 is ms i.e. alarm duration
        winsound.Beep(2500,1000)
    alarm=False

while True:
    _,frame=cap.read()
    frame=imutils.resize(frame,width=500)

    if alarm_mode:
        frame_bw=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame_bw=cv2.GaussianBlur(frame_bw,(5,5),0)

        difference=cv2.absdiff(frame_bw,start_frame)
        #every difference in pixel above 25 set it to 255(white) everything below 25 is set to 0(black)
        threshold=cv2.threshold(difference,25,255,cv2.THRESH_BINARY)[1]
        start_frame=frame_bw

    #checking if total sum of white pixels in image are greater than 300 indicating movement
        if threshold.sum()>300:
            alarm_counter+=1
        else:
            #if no movement is seen and counter>0
            if alarm_counter>0:

                alarm_counter-=1
        #show white regions indicating movement in a window called cam
        cv2.imshow("cam",threshold)

    else:
        #show originial frame if alarm mode is inactive
        cv2.imshow("Cam",frame)

    if alarm_counter>20:
        if not alarm:
            alarm=True
            threading.Thread(target=beep_alarm).start()

    key_pressed=cv2.waitKey(30)
    if key_pressed==ord("t"):
        alarm_mode=not alarm_mode
        alarm_counter=0

    if key_pressed==ord("q"):
        alarm_mode=False
        break
#release camera capture
cap.release()
#closing all opencv windows
cv2.destroyAllWindows()
