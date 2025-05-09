import cv2
import mediapipe as mp
import math
import serial 
from PIL import Image, ImageDraw

arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1) 
def write_read(x): 
    arduino.write(bytes(x, 'utf-8')) 
    
class pt():
    x=0
    y=0

def slop(a,b,c):
    ang = math.degrees(math.atan2(c.y-b.y, c.x-b.x) - math.atan2(a.y-b.y, a.x-b.x))
    return int(ang)
    
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

pt1=pt()
pt2=pt()
pt3=pt()
pt4=pt()
pt5=pt()

a1=0
a2=0
a3=0
p=pt()
p.x=1

hold=False
a4=0

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            results_pose = pose.process(image)
            
            try:
                pt1.x=1-results_pose.pose_landmarks.landmark[12].x
                pt1.y=1-results_pose.pose_landmarks.landmark[12].y
                pt2.x=1-results_pose.pose_landmarks.landmark[14].x
                pt2.y=1-results_pose.pose_landmarks.landmark[14].y
                try:
                    pt3.x=1-results.multi_hand_landmarks[0].landmark[0].x
                    pt3.y=1-results.multi_hand_landmarks[0].landmark[0].y
                    pt4.x=1-results.multi_hand_landmarks[0].landmark[4].x
                    pt4.y=1-results.multi_hand_landmarks[0].landmark[4].y
                    pt5.x=1-results.multi_hand_landmarks[0].landmark[8].x
                    pt5.y=1-results.multi_hand_landmarks[0].landmark[8].y
                    #print(results.multi_hand_landmarks[0].landmark[8].z)
                except:
                    pass
                p.y=pt1.y
                a1=30+slop(p,pt1,pt2)
                
                a2=slop(pt1,pt2,pt3)
                if a2<0:
                    a2=-a2-90
                else:
                    a2=270-a2
                
                a2=180-a2   
                a3=slop(pt2,pt3,pt4)-90
                print(hold)
                if hold:
                    if math.dist([pt3.x,pt3.y],[pt5.x,pt5.y])>0.2:
                        a4=0
                        hold=False
                else:
                    if math.dist([pt3.x,pt3.y],[pt5.x,pt5.y])<0.2:
                        a4=90
                        hold=True
                
            except Exception as e:      
                pass
                
            radius = 5
            color = (0, 0, 255) 
            thickness = -1

            center_coordinates = (int(image.shape[1]*(1-pt1.x)),int(image.shape[0]*(1-pt1.y)))
            image = cv2.circle(image, center_coordinates, radius, color, thickness)
            center_coordinates = (int(image.shape[1]*(1-pt2.x)),int(image.shape[0]*(1-pt2.y)))
            image = cv2.circle(image, center_coordinates, radius, color, thickness)
            center_coordinates = (int(image.shape[1]*(1-pt3.x)),int(image.shape[0]*(1-pt3.y)))
            image = cv2.circle(image, center_coordinates, radius, color, thickness)
            center_coordinates = (int(image.shape[1]*(1-pt4.x)),int(image.shape[0]*(1-pt4.y)))
            image = cv2.circle(image, center_coordinates, radius, color, thickness)
            center_coordinates = (int(image.shape[1]*(1-pt5.x)),int(image.shape[0]*(1-pt5.y)))
            image = cv2.circle(image, center_coordinates, radius, color, thickness)

            write_read(str(a1)+" "+str(a2)+" "+str(a3)+" "+str(a4))
            #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
           
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
arduino.close()
cap.release()

