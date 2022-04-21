import cv2
import os
import argparse

blur_threshold = 700

def check_blur(file):
    print(file)
    image = cv2.imread(file)
    score = cv2.Laplacian(image, cv2.CV_64F).var()
    if score < blur_threshold:
        print(score)
        os.remove(file)
        print("REMOVED")


def check_blur_directory(a_directory):
    for filename in os.listdir(a_directory):
        if not filename.startswith('.'):
            filepath = os.path.join(a_directory, filename)
            check_blur(filepath)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Program for erasing blury images - please use -d and the directory that should be checked')
    parser.add_argument("-d","--directory", help="include path to directory to be chekced")
    args = parser.parse_args()
    print(args.directory)
    check_blur_directory(args.directory)

    #check_blur_directory("/Users/ferbrjan/Downloads/PV1")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
