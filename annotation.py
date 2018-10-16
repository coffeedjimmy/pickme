import glob
import cv2
import numpy as np

L_TOP_X = 99999999
L_TOP_Y = 99999999
R_BOTTOM_X = 0
R_BOTTOM_Y = 0


def click(event, x, y, flags, param):
    global L_TOP_X
    global L_TOP_Y
    global R_BOTTOM_X
    global R_BOTTOM_Y

    if event == cv2.EVENT_LBUTTONDOWN:
        grid[y // BLOCK][x // BLOCK] = (grid[y // BLOCK][x // BLOCK] + 1) % 2

        if (y//BLOCK * BLOCK) < L_TOP_Y or (x//BLOCK * BLOCK) < L_TOP_X:
            L_TOP_Y = (y//BLOCK * BLOCK)
            L_TOP_X = (x//BLOCK * BLOCK)

        if (y//BLOCK * BLOCK + BLOCK) > R_BOTTOM_Y or (x//BLOCK * BLOCK + BLOCK) > R_BOTTOM_X:
            R_BOTTOM_Y = (y//BLOCK * BLOCK + BLOCK)
            R_BOTTOM_X = (x//BLOCK * BLOCK + BLOCK)


types = ('./data/*.jpg', './data/*.png')
img_files = []
for f_type in types:
    img_files.extend(glob.glob(f_type))

cv2.namedWindow('annotation')
cv2.setMouseCallback('annotation', click)


for img_file in img_files:

    L_TOP_X = 99999999
    L_TOP_Y = 99999999
    R_BOTTOM_X = 0
    R_BOTTOM_Y = 0

    img = cv2.imread(img_file)
    height, width, channels = img.shape

    BLOCK = width // 15 if width > height else height // 15

    COL = width // BLOCK + 1
    ROW = height // BLOCK + 1

    grid = np.zeros([ROW, COL], dtype=np.int)

    grid.fill(0)

    while True:

        visual = img.copy()

        for r in range(ROW):
            for c in range(COL):
                cv2.rectangle(visual, (c*BLOCK, r*BLOCK),
                              ((c+1)*BLOCK, (r+1)*BLOCK), (255, 255, 255), cv2.FILLED * grid[r][c])

        cv2.imshow('annotation', visual)

        if cv2.waitKey(2) == 32:
            fp_label = open('annotation.txt', 'a')
            fp_label.writelines(img_file + ',' + str(L_TOP_X) + ',' + str(L_TOP_Y) + ','
                                + str(R_BOTTOM_X) + ',' + str(R_BOTTOM_Y) + '\n')
            fp_label.close()
            break
