import os

def check_labels(root_dir, train_val):
    for item in train_val:
        images = os.path.join(root_dir, item, "images")
        labels = os.path.join(root_dir, item, "labels")
        for file in os.listdir(images):
            if "aug" in file:
                #class_id = file[0]
                label_file = os.path.join(labels, os.path.splitext(file)[0] + ".txt")
                with open(label_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                if not lines:
                    print(lines[0])
                    print("Negative", label_file)



if __name__ == "__main__":
    check_labels(
        root_dir="/home/apsu/TestSet",
        train_val=["train", "valid"]
    )
