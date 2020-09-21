import numpy as np
import cv2
cap = cv2.VideoCapture(0)


width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))

rect = (np.random.rand(2,2) * [width - 1, height -1 ] ).astype(int)
line = (np.random.rand(2,2) * [width, height] ).astype(int)
speed1 = np.array([[5, -2], [5, -2]])
speed2 = np.array([[2, -7], [6, -7]])


def norm(a, speed):
    speed = np.multiply(speed, ( (a+speed <= np.array([[width, width], [height, height]])) & (a+speed >= 0) ).astype(int) * 2 - 1  )
    return a + speed, speed

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # write the flipped frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        rect, speed1 = norm(rect, speed1)
        line, speed2 = norm(line, speed2)
        frame = cv2.flip(cv2.line(frame, tuple(rect[:, 0]),
                                  tuple(rect[:, 1]), (100,255,255), 7), 1)
        frame = cv2.rectangle(frame,  tuple(line[:, 0]),
                                  tuple(line[:, 1]), (255, 255, 100), 7)
        out.write(frame)

        cv2.imshow('frame',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break
    else:
        break

out.release()
cap.release()
cv2.destroyAllWindows()