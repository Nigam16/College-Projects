#import required library

import pymysql  # for mysql request to post in website
import cv2      # for image processing
import pandas as pd   # for reading file
import urllib.request  # for reading image from http (espcam)
import numpy as np      # for handling number
import os #to import the os module to interact
import time #to import time and date

from datetime import datetime
import face_recognition  # face recognition module
 
path = r'image_folder'  # folder where images are saved for face recognition
url='http://192.168.43.176/cam-mid.jpg'
##'''cam.bmp / cam-lo.jpg /cam-hi.jpg / cam.mjpeg '''

#Variables..............
counter_value=10
attendance_counter=counter_value
attendance_flag= False
 
images = []
classNames = []
myList = os.listdir(path)
# It will list out the images  available in folder for face recognition
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


#finction to encode image
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
 # funtion to make attendance -- it wills sent data to mysql
def markAttendance(name):
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="attendance"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT id FROM attendance WHERE Name= %s AND inout_flag= \"in\" ORDER BY id DESC LIMIT 1" , name )
    
    myresult = mycursor.fetchall()
    
    if myresult:  
      date_string = time.strftime('%Y-%m-%d %H:%M:%S')
      tuple1 = (date_string, name)
      print("GoodBye!!!    " +name)
      mycursor = mydb.cursor()
      mycursor.execute("UPDATE attendance SET checkout_at=%s, inout_flag='out'  WHERE Name= %s  ORDER BY id DESC LIMIT 1",tuple1)
      mydb.commit()
      
    else:
      print ("Welcome!!!   " +name)
      mycursor = mydb.cursor()
      sql = "INSERT INTO attendance (Name, inout_flag) VALUES (%s, 'in')"
      mycursor.execute(sql,name)
      mydb.commit()
      print(mycursor.rowcount, "record inserted.")

encodeListKnown = findEncodings(images)
print('Encoding Complete')
 
#cap = cv2.VideoCapture(0)

while True:
    #success, img = cap.read()
    img_resp=urllib.request.urlopen(url)
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgnp,-1)
# img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
 
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
# print(faceDis)
        matchIndex = np.argmin(faceDis)
 
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
# print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            if attendance_flag==False:
                markAttendance(name)
                attendance_flag=True
            if attendance_counter==0:
                attendance_flag=False
                attendance_counter=counter_value
            
            attendance_counter=attendance_counter-1
            print (attendance_counter)
                
 
    cv2.imshow('Webcam', img)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break
cv2.destroyAllWindows()
cv2.imread
