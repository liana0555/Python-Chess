import cv2
img_path = "c:\Users\User\Downloads\pictures"

img_list = []

for i in img_path:
    img = cv2.imread(i)
    img_list = img