import threading

import smtplib


import cv2

from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

haseeb = cv2.imread("Cheeb.jpg") 
seerat = cv2.imread("Seerat.png")

list_of_ppl = {
    "Haseeb": haseeb,
    "Seerat": seerat
}


face_match = False
previous_person = ''
person_in_frame = ''

def check_face(frame):
    global face_match
    global person_in_frame
    try:
        for name, img in list_of_ppl.items():
            result = DeepFace.verify(frame, img.copy()) 
            if result['verified']:
                face_match = True
                person_in_frame = name
                # print(f"OMG it's {name} >~<")
                break  # Stop checking after the first match
            else:
              face_match = False
              person_in_frame = ''
    except ValueError:
        face_match = False
        person_in_frame = ''


while True:
    
    
    ret, frame = cap.read()

    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1
        if face_match:
            cv2.putText(frame, f"OMG its {person_in_frame} >~<", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            if person_in_frame != previous_person:

                s = smtplib.SMTP('smtp.gmail.com', 587)
                # start TLS for security
                s.starttls()
                s.login("pyface.notification@gmail.com", "xxsj azep siyl psvr")
                message = f"{person_in_frame} is at the door."
                # sending the mail
                s.sendmail("pyface.notification@gmail.com", "haseebiqbal8143@gmail.com", message)

            # person_in_frame = previous_person
            previous_person = person_in_frame
        else:
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        s.quit()
        break

cap.release()
cv2.destroyAllWindows() 