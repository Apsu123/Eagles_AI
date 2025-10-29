from PIL import Image
import os

def convert_to_png(input_jpg_path, output_png_path):
    # Open the JPG image
    try:
        img = Image.open(input_jpg_path)
    except Image.UnidentifiedImageError:
        print(f"Error: {input_jpg_path} is not a valid image file.")
        return

    # Convert and save as PNG
    img.save(output_png_path, 'PNG')
    # Remove old non-PNG file if in the same folder
    input_dir = os.path.dirname(os.path.abspath(input_jpg_path))
    output_dir = os.path.dirname(os.path.abspath(output_png_path))
    if input_dir == output_dir and not input_jpg_path.lower().endswith('.png'):
        try:
            os.remove(input_jpg_path)
        except OSError:
            pass

if __name__ == "__main__":

    root_folder = "/home/apsu/FieldTest/Backgrounds4 (Copy)"

    for file in os.listdir(root_folder):

            print(f"Processing file: {file}")
            file_path = os.path.join(root_folder, file)

            convert_to_png(
                file_path,
                os.path.splitext(file_path)[0] + '.png'
            )
