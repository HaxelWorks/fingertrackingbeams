import cv2
import mediapipe as mp
from dmx import flint8,move_mirrors
import time
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

CAM = 1
wCam, hCam = (1920, 1080)

PARTS = (18,22,17,21)



def maprange( a, b, s):
	(a1, a2), (b1, b2) = a, b
	return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))
mapx = lambda x: maprange((-0.15,0.65),(0,1),x)
mapy = lambda y: maprange((0,-0.7),(1,0),y)

def filter_parts(parts):
    global ma, mi
    if parts.pose_landmarks:
        parts = parts.pose_world_landmarks.landmark
        # print([f"x:{parts[i].x:.1f} y:{parts[i].y:.1f}" for i in PARTS if not parts[i] is None])
        
        
        print((parts[22].y > parts[16].y,parts[21].y > parts[17].y))
            
        return [[flint8(mapx(m*parts[i].x)),flint8(mapy(parts[i].y))] for m,i in zip([-1,-1,1,1],PARTS) if not parts[i] is None]
    else:
        return [[128,128] for _ in PARTS]
    






# For webcam input:
pTime=0
cap = cv2.VideoCapture(CAM)
cap.set(3, wCam)
cap.set(4, hCam)
with mp_pose.Pose(
    model_complexity = 1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    # image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    if results := pose.process(image):
        parts = filter_parts(results)
        parts[0][0] = 255-parts[0][0]
        parts[2][0] = 255-parts[2][0]
        # print(parts)
        move_mirrors(*parts)
        
    
    
    
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(image,str(int(fps)),(20,50), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()