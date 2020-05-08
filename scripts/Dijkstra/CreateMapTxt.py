#!/usr/bin/env python
import cv2

# Read Height map
img = cv2.imread("../meshes/Heightmapnew.png", 0)
height, width = img.shape
print(height, width)

file = open("map.txt", "w")
# Write all values to a text file
for i in range(height):
    line = ""
    for j in range(width):
        if j == width-1:
            line += str(img[i][j])
        else:
            line += str(img[i][j])+","
    file.write(line+"\n")

file.close()
cv2.imshow("img", img)
cv2.waitKey(0)
