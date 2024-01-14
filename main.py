import math
import face_recognition
import cv2
import numpy as np
from ultralytics import YOLO
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import time

# Initialize Firebase
cred = credentials.Certificate('service_accnt_creds.json')
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()


def call_recognition(): 
    # Read data
    doc_ref = db.collection('garbage').document('garbage')
    try:
        doc = doc_ref.get()
        if doc.exists:
            print('Document data:', doc.to_dict())
        else:
            print('No such document!')
    except Exception as e:
        print('Error reading document:', e)
    # Get a reference to webcam #0 (the default one)
    # video_capture = cv2.VideoCapture('rtmp://global-live.mux.com/app/c6b6776b-450f-4e60-df73-ac6b146d0517')
    ret = None
    while not ret:
        print("Trying to get video capture")
        video_capture = cv2.VideoCapture('rtmp://global-live.mux.com:5222/app/c6b6776b-450f-4e60-df73-ac6b146d0517')
        ret, frame = video_capture.read()
        time.sleep(5)
    print("Succeeded!")

    # Load a sample picture and learn how to recognize it.
    linda_image = face_recognition.load_image_file("linda.jpg")
    linda_face_encoding = face_recognition.face_encodings(linda_image)[0]

    # Load a second sample picture and learn how to recognize it.
    stanley_image = face_recognition.load_image_file("stanley.jpg")
    stanley_face_encoding = face_recognition.face_encodings(stanley_image)[0]

    jenny_image = face_recognition.load_image_file("jenny.jpg")
    jenny_face_encoding = face_recognition.face_encodings(jenny_image)[0]

    andy_image = face_recognition.load_image_file("andy.jpg")
    andy_face_encoding = face_recognition.face_encodings(andy_image)[0]

    nikhil_image = face_recognition.load_image_file("nikhil.png")
    nikhil_face_encoding = face_recognition.face_encodings(nikhil_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        linda_face_encoding,
        stanley_face_encoding,
        nikhil_face_encoding,
        jenny_face_encoding,
        andy_face_encoding
    ]
    known_face_names = [
        "Linda",
        "Stanley", 
        "Nikhil", 
        "Jenny", 
        "Andy"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                "teddy bear", "hair drier", "toothbrush"
                ]
    model = YOLO("yolo-Weights/yolov8n.pt").cuda()

    count = 0
    frequency = 10

    while True:
        # Grab a single frame of video
        is_facial = doc_ref.get().to_dict()["facial"] == True

        count += 1
        ret, frame = video_capture.read()
        if frame is None: 
            print("Failed")
            break

        # Only process every other frame of video to save time
        if count % frequency == 0:

            if not is_facial:
            # if is_facial:
                results = model(frame, stream=True)
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        # bounding box
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                        # put box in cam
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                        # confidence
                        confidence = math.ceil((box.conf[0]*100))/100
                        print("Confidence --->",confidence)

                        # class name
                        cls = int(box.cls[0])
                        print("Class name -->", classNames[cls])

                        # object details
                        org = [x1, y1]
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        fontScale = 1
                        color = (255, 0, 0)
                        thickness = 2

                        cv2.putText(frame, classNames[cls], org, font, fontScale, color, thickness)

                        if cls == "suitcase":
                            db.collection('object_detection').document('names').set({
                                'detected': "did you check in for your flight?"
                            })
                            # doc_ref = db.collection('face_recognition_names').document('names')
                            # doc_ref.set({
                            #     'name_output': name
                            # })
            else:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                # rgb_small_frame = small_frame[:, :, ::-1]
                rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
                # rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        print(name)
                        db.collection('face_recognition_names').document('names').set({
                            'name_output': name
                        })

                    face_names.append(name)


        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        # cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()
    
    # return name

# if is_facial: 
name = call_recognition()
# else: 
#     # object_detection()
#     pass

class Memory:
    def __init__(self, name, description):
        self.name = name
        # context = number of interactions
        self.context = 0
        self.description = description
    
    def increment_context(self): 
        self.context += 1 
    
    def get_context(self): 
        return self.context

    def get_name(self): 
        return self.name

    def get_description(self): 
        return self.description

linda = Memory("Linda", "Pronouns: She/her. Freshman at Harvard. CS Major. Interested in Sebastion Thrun (not like that)")
stanley = Memory("Stanley", "Pronouns: He/him. Junior at Stanford. CS Major. Interested in Sebastion Thrun (not like that)")
jenny = Memory("Jenny", "Pronouns: He/him. Junior at Stanford. CS Major. Interested in Sebastion Thrun (not like that)")
nikhil = Memory("Nikhil", "Pronouns: He/him. Junior at Stanford. CS Major. Interested in Sebastion Thrun (not like that)")
andy = Memory("Andy", "Pronouns: He/him. Junior at Stanford. CS Major. Interested in Sebastion Thrun (not like that)")

    
# Release handle to the webcam


#------------------------------------------------Handling firebases------------------------------------------------

# Add data