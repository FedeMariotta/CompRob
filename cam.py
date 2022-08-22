import cv2

cap = cv2.VideoCapture(-1)

while (True):
    #cap.set(10,15)
    ret, frame = cap.read()
    cv2.imshow('camara', frame)