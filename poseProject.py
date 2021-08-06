import cv2
import PoseModule as pm
import time
import numpy as np

# OpenCV video load
cap = cv2.VideoCapture("resource/weight_lift.mp4")
# Get web camera default is 0
# cap = cv2.VideoCapture(0)
# # Set web camera size, 3 means width and 4 means height
# cap.set(3, 1194)
# cap.set(4, 890)

# FPS initial value
pTime = 0
downScaleRatio = 0.6
draw_scale = 8

# Create object
detector = pm.poseDetector()
# 利用angle的增加和减少来判断direction，当完成一次up和down的时候，算一次count
# 所以需要设置up和down的临界值，需要是一个范围，比如up的从170度开始减少，从50度开始增加
# 找减少的最小值和增加的最大值
count_left = 0
dir_left = 0

count_right = 0
dir_right = 0

# Angle threshold
angle_min = 70
angle_max = 150

while True:
    # success return True or False to indicate whether video ends
    success, img = cap.read()
    # Using waitkey to control the intersection time of sequence images
    if (cv2.waitKey(1) & 0xFF == ord('q')) | success == False:
        # df = pd.DataFrame(angle_vector)
        # df.to_csv("agnles.csv")
        break
    # Get image real dimension
    height, width, channels = img.shape
    img = cv2.resize(img, (int(width * downScaleRatio), int(height * downScaleRatio)))
    print(height, width)
    # Get rescaled dimension
    h, w, _ = img.shape
    # Run Pose Estimation
    detector.findPose(img, draw=False)
    # Get pose key points coordinates
    lmList = detector.findPosition(img, draw=False)
    # Get index for certain position
    if lmList is not None and len(lmList) > 0:
        # Get left arm points
        point1 = (lmList[12][1], lmList[12][2])
        point2 = (lmList[14][1], lmList[14][2])
        point3 = (lmList[16][1], lmList[16][2])
        # Draw left arm key points
        img = detector.drawAngle(img, point1, point2, point3)
        # Get left arm angle
        angle_left = detector.calculateAngle(point1, point2, point3, acuteAngle=True)
        # Get right arm points
        point1 = (lmList[11][1],lmList[11][2])
        point2 = (lmList[13][1], lmList[13][2])
        point3 = (lmList[15][1], lmList[15][2])
        # Draw right arm key points
        img = detector.drawAngle(img, point1, point2, point3)
        # Get right arm angle
        angle_right = detector.calculateAngle(point1, point2, point3, acuteAngle=True)

        # Based on the threshold to accumulate count
        # Left arm count
        if angle_left > angle_max:
            if dir_left == 0:
                count_left += 0.5
                dir_left = 1
        if angle_left < angle_min:
            if dir_left == 1:
                count_left += 0.5
                dir_left = 0

        # Right arm count
        if angle_right > angle_max:
            if dir_right == 0:
                count_right += 0.5
                dir_right = 1
        if angle_right < angle_min:
            if dir_right == 1:
                count_right += 0.5
                dir_right = 0

        # Set bounding box size
        box_length = int(h / draw_scale) if h / draw_scale > w / draw_scale else int(w / 6)

        # Left side Bounding box and Text
        cv2.rectangle(img, (0, int(h - 3 * box_length / 4)), (box_length, h), (141, 143, 141), 3)
        cv2.putText(img, f'{int(count_left)}', (int(box_length / (3 * draw_scale)), h - int(box_length / (draw_scale))),
                    cv2.FONT_HERSHEY_PLAIN, int(box_length / 20), (13, 129, 252), int(box_length / 20))
        # Text indicate side
        cv2.putText(img, "L", (int(box_length / 3), int(h - 3 * box_length / 4 - box_length / (draw_scale))),
                    cv2.FONT_HERSHEY_PLAIN, int(box_length / 30), (13, 129, 252), int(box_length / 30))

        # Draw a bar
        bar = np.interp(angle_left, (angle_min,angle_max), (int(h - 3 * box_length / 4 - box_length / (draw_scale) - box_length * 3),
                                               int(h - 3 * box_length / 4 - box_length / (draw_scale))))
        cv2.rectangle(img, (0, int(h - 3 * box_length / 4 - box_length / (draw_scale))),
                      (int(box_length / 4), int(h - 3 * box_length / 4 - box_length / (draw_scale) - box_length * 3)),
                      (141, 143, 141), int(box_length / 50))
        cv2.rectangle(img, (int(1 / draw_scale), int(bar)),
                      (int(box_length / 4), int(h - 3 * box_length / 4 - box_length / (draw_scale))), (13, 129, 252),
                      cv2.FILLED)

        # Draw percentage
        per = np.interp(angle_left, (angle_min,angle_max), (100, 0))
        cv2.putText(img, f'{int(per)}%',
                    (int(1 / draw_scale), int(h - 3 * box_length / 4 - 2 * box_length / (draw_scale) - box_length * 3)),
                    cv2.FONT_HERSHEY_PLAIN, int(box_length / 60), (13, 129, 252), int(box_length / 60))
        # Right side Bounding box and Text
        cv2.rectangle(img, (int(w - box_length), int(h - 3 * box_length / 4)), (w, h), (141, 143, 141), 3)
        cv2.putText(img, f'{int(count_right)}',
                    (int(w - box_length + box_length / (3 * draw_scale)), int(h - box_length / (draw_scale))),
                    cv2.FONT_HERSHEY_PLAIN, int(box_length / 20), (13, 129, 252), int(box_length / 20))
        # Text indicate side
        cv2.putText(img, "R", (int(w - 2 * box_length / 3), int(h - 3 * box_length / 4 - box_length / (draw_scale))),
                    cv2.FONT_HERSHEY_PLAIN, int(box_length / 30), (13, 129, 252), int(box_length / 30))

        # Draw a bar
        bar = np.interp(angle_right, (angle_min,angle_max), (
        int(h - 3 * box_length / 4 - box_length / (draw_scale) - box_length * 3),
        int(h - 3 * box_length / 4 - box_length / (draw_scale))))
        cv2.rectangle(img, (int(w - box_length / 4), int(h - 3 * box_length / 4 - box_length / (draw_scale))),
                      (int(w), int(h - 3 * box_length / 4 - box_length / (draw_scale) - box_length * 3)),
                      (141, 143, 141), int(box_length / 50))
        cv2.rectangle(img, (int(w - box_length / 4 - 1 / draw_scale), int(bar)),
                      (int(w), int(h - 3 * box_length / 4 - box_length / (draw_scale))), (13, 129, 252), cv2.FILLED)

        # Draw percentage
        per = np.interp(angle_right, (angle_min,angle_max), (100, 0))
        cv2.putText(img, f'{int(per)}%', (
        int(w - box_length / 2), int(h - 3 * box_length / 4 - 2 * box_length / (draw_scale) - box_length * 3)),
                    cv2.FONT_HERSHEY_PLAIN, int(box_length / 60), (13, 129, 252), int(box_length / 60))

    # Add frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, "FPS:" + str(int(fps)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, int(box_length / 80), (145, 145, 145), int(box_length / 80))
    # it shows Video as a sequence of images
    cv2.imshow("Video", img)