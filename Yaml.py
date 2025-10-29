import yaml
import os

def generate_yaml(input_folder, output_yaml_path, train_images_path, val_images_path, serials_path):
    classes = []
    with open(serials_path, 'r') as file:
        serials = [line.strip() for line in file if line.strip()]
        for line in serials:
            if line == "NEGATIVE":
                break
            classes.append(line)

    data = {
        'names': classes,
        'nc': len(classes),
        'train': train_images_path,
        'val': val_images_path
    }
    with open(output_yaml_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

# Call the function with the original paths
if __name__ == "__main__":
    generate_yaml(
        input_folder="/home/apsu/Test/Raw",
        output_yaml_path='/home/apsu/Test/Modified/data.yaml',
        train_images_path='/home/apsu/LegoDetect/Annotated/train/images',
        val_images_path='/home/apsu/LegoDetect/Annotated/valid/images',
        serials_path='/home/apsu/FieldTest/serials.txt'
    )


