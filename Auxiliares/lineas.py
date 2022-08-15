import cv2
import numpy as np

vid = cv2.VideoCapture(2)#En odroid la camara suele ser -1
  
while(True):
    ret, frame = vid.read()
  
    # Display the resulting frame
    cv2.imshow('frame', frame)

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    lines = cv2.HoughLinesP(edges,2,np.pi/90,100,minLineLength=100,maxLineGap=10)
    try:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
            #cv2.imshow('Bordes de Imagen', edges)
            cv2.imshow('frame', frame)
    except:
        print("No se encontraron lineas")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()