import math
import cv2
import mediapipe
import time
import numpy as np
import hNDMODULE as hm
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap=cv2.VideoCapture(0)
cap.set(3,1000)
cap.set(4,1000)
cTime = 0
pTime = 0
vol=0;
volbar=150
volp=0

detector=hm.handDetector(detectionCon=0.7)
while True:
    suc,img=cap.read()
    img=detector.findHands(img,draw=True)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    #volume.GetMute()
    #volume.GetMasterVolumeLevel()
    print(volume.GetVolumeRange())


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,((x2+x1)//2,(y1+y2)//2),10,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        dis=math.hypot((x2-x1),(y2-y1))
        vol=np.interp(dis,[20,350],[-65.25,0])
        volbar=np.interp(dis,[20,350],[400,150])
        volp=np.interp(dis,[20,350],[0,100])
        cv2.putText(img,str(int(volp)),(30,140),cv2.FONT_HERSHEY_TRIPLEX,1,(255,0,0),3)
        volume.SetMasterVolumeLevel(int(vol), None)
        cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
        cv2.rectangle(img,(50,int(volbar)),(85,400),(255,0,0),cv2.FILLED)
        if(dis<20):
            cv2.circle(img,((x2+x1)//2,(y1+y2)//2),10,(0,255,0),cv2.FILLED)

        #print(dis)
        #min 20
        #max 300
    cv2.imshow("img",img)
    cv2.waitKey(1)