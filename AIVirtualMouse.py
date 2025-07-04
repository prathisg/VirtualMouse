import cv2
import numpy as np
import HandTracking as ht
import time
import autopy

wCam,hCam = 640,480
frameR=60
smoothening = 7
cap= cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pTime = 0
plocX,plocY = 0,0
clocX,clocY = 0,0
detector = ht.handDetector(maxHands=1)
wScr,hScr = autopy.screen.size()
print(f"window size {wScr},{hScr}")

while True:
    #1. find hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList,bbox = detector.findPosition(img)

    #2.get tip of index & middle

    if len(lmList)!=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        #print(x1,y1,x2,y2)
    
        #3.check fingerup
        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-2*frameR),(255,0,0),2)

        #4.Only index -moving
        if fingers[1]==1 and fingers[2]==0:

            #5.convert coords
            x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(y1,(frameR,hCam-frameR),(0,hScr))
            #6.smoothen
            clocX = plocX+(x3 - plocX)/smoothening
            clocY = plocY+(y3 - plocY)/smoothening
            #7.move mouse
            autopy.mouse.move(wScr-clocX, clocY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX, plocY = clocX, clocY

        #8. Both Index and middle - up => Clicking
        if fingers[1]==1 and fingers[2]==1:
            #9. find dist btw fingers
            length, img, lineInfo= detector.findDistance(8,12,img)
            print(length)  
            #10. Click mouse if distance short
            if length<35:
                cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,255),cv2.FILLED)
                autopy.mouse.click()
    
    
    #11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,40),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    
    #12.Display
    cv2.imshow("Image",img)
    cv2.waitKey(1)