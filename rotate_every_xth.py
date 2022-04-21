import cv2
import os
import argparse

def rotate_dir(directory,rotation):
    for filename in os.listdir(directory):
        if not filename.startswith('.'):
            filepath = os.path.join(directory, filename)
            image = cv2.imread(filepath)
            (h, w) = image.shape[:2]
            (cX, cY) = (w // 2, h // 2)
            if rotation == "R":
                M = cv2.getRotationMatrix2D((cX, cY), -90, 1.0)
            elif rotation == "L":
                M = cv2.getRotationMatrix2D((cX, cY), 90, 1.0)
            elif rotation == "0":
                M = cv2.getRotationMatrix2D((cX, cY), 0, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h))
            gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(filepath,gray)

def erase_dir(directory,number):
    cnt = 0
    for filename in os.listdir(directory):
        if not filename.startswith('.'):
            cnt+=1
            filepath = os.path.join(directory, filename)
            if (cnt%int(number)) != 0:
                os.remove(filepath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for rotating images and selecting every x-th - please use -d and the directory that should be processed')
    parser.add_argument("-d","--directory", help="include path to directory to be processed")
    parser.add_argument("-r", "--rotation", help="L/R/0 based on the direction of desired rotation")
    parser.add_argument("-n", "--number", help="number of images to be skipped - 5 -> every fifth image will be kept")

    args = parser.parse_args()
    print(args.directory)
    print(args.rotation)
    print(args.number)

    rotate_dir(args.directory,args.rotation)
    print("DIRECTORY ROTATED")
    if int(args.number) != 0:
        erase_dir(args.directory,args.number)
        print("DIRECTORY ERASED")