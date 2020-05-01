import cv2

img = cv2.imread("../meshes/Heightmapnew.png", 0)
height, width = img.shape
print(height, width)

file = open("map.txt", "w")

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
