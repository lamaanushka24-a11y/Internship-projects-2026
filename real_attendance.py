import cv2
import os
from datetime import datetime

# Load the built-in face tracking model profile
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Boot up the web camera
cap = cv2.VideoCapture(0)

print("Initializing live camera stream... Press 'q' on your keyboard to close.")

log_file = "Attendance_Log.csv"

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to grab camera frame.")
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "STUDENT PRESENT", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        if not os.path.exists(log_file):
            with open(log_file, "w") as f:
                f.write("Date,Time,Status\n")
                
        with open(log_file, "a") as f:
            f.write(f"{date_str},{time_str},PRESENT\n")

    cv2.imshow('AI Attendance System - Live Cam', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Camera stream closed safely.")
