# Importing Required Modules
from rembg import remove
from PIL import Image
import os


def make_image_transparent(input_path, output_path):
    # Processing the image
    try:
        input = Image.open(input_path)
    except Image.UnidentifiedImageError:
        os.remove(input_path)
        return

    # Removing the background from the given Image
    img= remove(input)



    rgba = img.convert("RGBA")

    datas = rgba.getdata()


    newData = []


    for item in datas:


       if item[0] == 0 and item[1] == 0 and item[2] == 0:


           newData.append((255, 255, 255, 0))


       else:


          newData.append(item)

    rgba.putdata(newData)
    rgba.save(output_path, "PNG")
    #Saving the image in the given path


if __name__ == "__main__":

        """
            TRAIN_VAL = ["train", "valid"]
            output_folder = "/home/apsu/FieldTest/DS"
        
            for item in TRAIN_VAL:
                    images = os.path.join("")

        for file in os.listdir(images):

            make_image_transparent(

                input_path=os.path.join(images, file),
                output_path=os.path.join(images, file)
            )"""


        for dirpath, dirnames, filenames in os.walk("/home/apsu/FieldTest/Raw"):
                for file in filenames:
                    file_path = os.path.join(dirpath, file)
                    make_image_transparent(
                        file_path,
                        file_path
                    )