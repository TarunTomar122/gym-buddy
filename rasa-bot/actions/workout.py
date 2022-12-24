import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

language = 'en'

# Create a Recognizer object
r = sr.Recognizer()


# print(sys.argv)

mp_pose = mp.solutions.pose

pose_image = mp_pose.Pose(static_image_mode=True,
                          min_detection_confidence=0.5)

pose_video = mp_pose.Pose(static_image_mode=False,
                          min_detection_confidence=0.7,
                          min_tracking_confidence=0.7)

mp_drawing = mp.solutions.drawing_utils


def detectPose(image_pose, pose, draw=False, display=False):
    original_image = image_pose.copy()
    image_in_RGB = cv2.cvtColor(image_pose, cv2.COLOR_BGR2RGB)
    resultant = pose.process(image_in_RGB)

    if resultant.pose_landmarks and draw:
        mp_drawing.draw_landmarks(image=original_image,
                                  landmark_list=resultant.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 255),
                                                                               thickness=2, circle_radius=2),
                                  connection_drawing_spec=mp_drawing.DrawingSpec(color=(49, 125, 237),
                                                                                 thickness=2, circle_radius=2))
    if display:
        plt.figure(figsize=[22, 22])
        plt.subplot(121)
        plt.imshow(image_pose[:, :, ::-1])
        plt.title("Input Image", size=14)
        plt.axis('off')
        plt.subplot(122)
        plt.imshow(original_image[:, :, ::-1])
        plt.title("Pose detected Image", size=14)
        plt.axis('off')
        plt.show()
    else:
        return original_image, resultant


def calculate_distance(pose1, pose2):
    total_distance = 0

    for i in range(len(pose1.pose_landmarks.landmark)):
        distance = np.linalg.norm(np.array([pose1.pose_landmarks.landmark[i].x, pose1.pose_landmarks.landmark[i].y, pose1.pose_landmarks.landmark[i].z]) - np.array(
            [pose2.pose_landmarks.landmark[i].x, pose2.pose_landmarks.landmark[i].y, pose2.pose_landmarks.landmark[i].z]))
        total_distance += distance
    return total_distance


def comparePose(first, second, pose):

    try:
        image_in_RGB = cv2.cvtColor(first, cv2.COLOR_BGR2RGB)
        first_result = pose.process(image_in_RGB)
        image_in_RGB = cv2.cvtColor(second, cv2.COLOR_BGR2RGB)
        second_result = pose.process(image_in_RGB)

        # Assume pose1 and pose2 are Packet objects returned by the PoseEstimationCalculator
        distance = calculate_distance(first_result, second_result)

        # print(f"The total distance between the poses is {distance}")
        return distance

    except:
        pass


def mainFunction(reps, exercise):

    down_image = './actions/down.png'
    # second_down = "./test.png"
    down = cv2.imread(down_image)

    up_image = './actions/up.png'
    up = cv2.imread(up_image)

    cap = cv2.VideoCapture(0)

    count = 0

    flag = False

    myobj = gTTS(
        text="Let's start bestie", lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # audio
    myobj.save("audio.mp3")

    audio_file = 'audio.mp3'
    playsound(audio_file)
    os.remove("audio.mp3")

    # While loop
    while True:

        # Capture frame-by-frame
        ret, frame = cap.read()

        # Show the captured image
        # cv2.imshow('WebCam', frame)

        if count >= int(reps):
            myobj = gTTS(
                text="good job bestie", lang=language, slow=False)

            # Saving the converted audio in a mp3 file named
            # audio
            myobj.save("audio.mp3")

            # Playing the converted file
            playsound(audio_file)
            os.remove("audio.mp3")
            break

        # wait for the key and come out of the loop
        if cv2.waitKey(1) == ord('q'):
            break

        downDistance = comparePose(down, frame, pose_image)
        upDistance = comparePose(up, frame, pose_image)

        # if downDistance:
        #     print("down distance", downDistance)

        # if upDistance:
        #     print("up distance", upDistance)

        if downDistance and not flag:
            if downDistance < 15:
                flag = True
                continue

        if upDistance and flag:
            if upDistance < 12:
                count += 1
                # print("Rep no.", count)

                myobj = gTTS(
                    text=str(count), lang=language, slow=False)

                # Saving the converted audio in a mp3 file named
                # welcome
                audio_file = 'audio.mp3'
                myobj.save("audio.mp3")

                # Playing the converted file
                playsound(audio_file)
                os.remove("audio.mp3")

                if count == 5:
                    myobj = gTTS(
                        text="Almost there...", lang=language, slow=False)

                    # Saving the converted audio in a mp3 file named
                    # audio
                    myobj.save("audio.mp3")

                    # Playing the converted file
                    playsound(audio_file)
                    os.remove("audio.mp3")

                flag = False
                continue

    # Discussed below
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    pass
