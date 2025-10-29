import os


def create_empty_labels(images, labels):
    for file in os.listdir(images):
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
            label_file = os.path.join(labels, os.path.splitext(file)[0] + ".txt")
            print(label_file)
            if not os.path.exists(label_file):
                open(label_file, "w").close()  # create empty file


if __name__ == "__main__":
    create_empty_labels(
        images="/home/apsu/LegoDetect/TestOutput/train/images",
        labels="/home/apsu/LegoDetect/TestOutput/train/labels",
    )
