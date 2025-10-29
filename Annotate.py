from autodistill_grounding_dino import GroundingDINO
from autodistill.detection import CaptionOntology
import os
import sys

sys.path.append('/home/apsu/PycharmProjects/Tools/')
from TestReplace import rewrite_first_char

def annotate_dataset(root_dir, output_folder):
    count = 0

    for entry in os.listdir(root_dir):
        full_path = os.path.join(root_dir, entry)
        if os.path.isdir(full_path):
            print(f"Folder: {entry}")

            ontology = CaptionOntology({
                f"LEGO part {count}": entry
            })

            base_model = GroundingDINO(ontology=ontology)
            input_folder = full_path
            base_model.label(input_folder=input_folder, output_folder=output_folder)
            count += 1

    TRAIN_VAL = ["train", "valid"]

    for item in TRAIN_VAL:
        images = os.path.join(output_folder, item, "images")
        labels = os.path.join(output_folder, item, "labels")

        for file in os.listdir(images):
            class_id = file[0]
            label_file = os.path.join(labels, os.path.splitext(file)[0] + ".txt")
            print(label_file)
            if not os.path.exists(label_file):
                continue
            rewrite_first_char(label_file, None, class_id)

        for file in os.listdir(images):
            if "NEG" in file:
                label_file = os.path.join(labels, os.path.splitext(file)[0] + ".txt")
                print(label_file)
                open(label_file, "w").close()

# Call the function with the original paths
if __name__ == "__main__":
    annotate_dataset(
        root_dir="/home/apsu/FieldTest/Raw",
        output_folder="/home/apsu/FieldTest/DS"
    )
