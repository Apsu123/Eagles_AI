# --- Import all functionality from other files ---
import os
import shutil
import random
from typing import List, Optional
from pathlib import Path

from AddBG import add_background_to_foreground
from AnnFromBin import annotate_dataset
from Augment import augment_dataset
from Convert import convert_to_png
from Get_Images import get_images_with_colors, download_image as download_image_with_colors
from Get_Images2 import get_images, download_image as download_image2
from RemoveBg import remove_background_from_folder
from Resize import resize_and_rename_images, resize_image
from ShowBox import show_boxes_on_images
from transparent import make_image_transparent
from Yaml import generate_yaml
from RemoveContent import clear_folder_contents
import time


class DatasetProcessor:
    """Main class to handle the dataset processing pipeline."""
    
    def __init__(self, base_output_dir: str = "/home/apsu/FieldTest/DS5"):
        self.base_output_dir = Path(base_output_dir)
        self.raw_dir = Path("/home/apsu/FieldTest/Raw2")
        self.backgrounds_dir = Path("/home/apsu/FieldTest/Backgrounds6")
        self.backgrounds_dir2 = Path("/home/apsu/FieldTest/Backgrounds7")
        self.train_val_folders = ["train", "valid"]
        
    def download_part_images(self) -> None:
        """Download images of parts with colors and negatives."""
        try:
            print("GETTING IMAGES OF PARTS".upper())
            
            # Download images with colors
            get_images_with_colors(
                serials_path='/home/apsu/FieldTest/serials.txt',
                output_dir=str(self.raw_dir),
                colors_path='/home/apsu/FieldTest/colors.txt',
            )

            get_images_with_colors(
                serials_path='/home/apsu/FieldTest/negatives2.txt',
                output_dir=str(self.raw_dir),
            )

            print("FINISHED GETTING IMAGES OF PARTS.".upper())

        except Exception as e:
            print(f"Error downloading part images: {e}")
            raise

    def download_background_images(self) -> None:
        """Download background images."""
        try:
            print("GETTING IMAGES OF BACKGROUNDS".upper())

            get_images(
                "many random LEGO pieces on white background top view",
                30,
                str(self.backgrounds_dir),
            )

            print("FINISHED GETTING IMAGES OF BACKGROUNDS.".upper())

        except Exception as e:
            print(f"Error downloading background images: {e}")
            raise

    def resize_images(self) -> None:
        """Resize and rename images in raw and backgrounds directories."""
        try:
            # Resize part images
            resize_and_rename_images(str(self.raw_dir), "/home/apsu/FieldTest/serials.txt", width=640, height=640)
            resize_and_rename_images(str(self.raw_dir), "/home/apsu/FieldTest/negatives2.txt", width=640, height=640)
            print("RESIZED AND RENAMED PART IMAGES.".upper())

        except Exception as e:
            print(f"Error resizing images: {e}")
            raise
    
    def convert_backgrounds_to_png(self) -> None:
        """Convert all background images to PNG format."""
        try:
            for file_path in self.backgrounds_dir.rglob("*"):
                if file_path.is_file():
                    convert_to_png(
                        str(file_path),
                        str(file_path.with_suffix('.png'))
                    )
            print("CONVERTED BACKGROUND IMAGES TO PNG.".upper())
            
        except Exception as e:
            print(f"Error converting backgrounds to PNG: {e}")
            raise
    
    def remove_backgrounds_from_parts(self) -> None:
        """Remove backgrounds from all part images."""
        try:
            for subfolder in self.raw_dir.iterdir():
                if subfolder.is_dir():
                    remove_background_from_folder(str(subfolder))
            print("REMOVED BACKGROUNDS FROM PART IMAGES.".upper())
            
        except Exception as e:
            print(f"Error removing backgrounds from parts: {e}")
            raise
    
    def annotate_dataset(self) -> None:
        """Annotate the dataset."""
        try:
            annotate_dataset(str(self.raw_dir), str(self.base_output_dir))
            print("ANNOTATED DATASET.".upper())
            
        except Exception as e:
            print(f"Error annotating dataset: {e}")
            raise
    
    def make_images_transparent(self) -> None:
        """Make all part images transparent."""
        try:
            for folder in self.train_val_folders:
                images_dir = self.base_output_dir / folder / "images"
                if not images_dir.exists():
                    continue
                    
                for file_path in images_dir.iterdir():
                    if file_path.is_file():
                        make_image_transparent(str(file_path), str(file_path))
            
            print("MADE PART IMAGES TRANSPARENT.".upper())
            
        except Exception as e:
            print(f"Error making images transparent: {e}")
            raise
    
    def augment_dataset(self) -> None:
        split = 0.8
        train = 30
        """Augment the dataset for both train and validation sets."""
        try:
            for folder in self.train_val_folders:
                images_dir = self.base_output_dir / folder / "images"
                labels_dir = self.base_output_dir / folder / "labels"

                if folder  == "train":
                    num_augmented = train
                else:
                    num_augmented = int((train-(train*split))/split)
                
                if not images_dir.exists() or not labels_dir.exists():
                    continue
                
                print(f"{(str(images_dir) + ' ' + str(labels_dir)).upper()}")
                
                augment_dataset(
                    images_dir=str(images_dir),
                    labels_dir=str(labels_dir),
                    num_augmented=num_augmented
                )
            
            print("AUGMENTED DATASET.".upper())
            
        except Exception as e:
            print(f"Error augmenting dataset: {e}")
            raise
    
    def convert_parts_to_png(self) -> None:
        """Convert all part images to PNG format."""
        try:
            for folder in self.train_val_folders:
                images_dir = self.base_output_dir / folder / "images"
                if not images_dir.exists():
                    continue
                    
                for file_path in images_dir.iterdir():
                    if file_path.is_file():
                        convert_to_png(
                            str(file_path),
                            str(file_path.with_suffix('.png'))
                        )
            
            print("CONVERTED PART IMAGES TO PNG AND RESIZED.".upper())
            
        except Exception as e:
            print(f"Error converting parts to PNG: {e}")
            raise
    
    def resize_backgrounds_again(self) -> None:
        """Resize background images again."""
        try:
            for file_path in self.backgrounds_dir.iterdir():
                if file_path.is_file():
                    resize_image(str(file_path))
            for file_path in self.backgrounds_dir2.iterdir():
                if file_path.is_file():
                    resize_image(str(file_path))
        except Exception as e:
            print(f"Error resizing backgrounds again: {e}")
            raise

    def resize_parts(self) -> None:
        """Resize part images."""
        try:
            for file_path in self.raw_dir.iterdir():
                scale = random.randint(64,640)
                if file_path.is_file():
                    resize_image(str(file_path), scale, scale)

                print("RESIZED BACKGROUND IMAGES AGAIN.".upper())
        except Exception as e:
            print(f"Error resizing parts: {e}")
            raise
    
    def add_backgrounds_to_parts(self) -> None:
            """Add random backgrounds to all part images."""
            for folder in self.train_val_folders:
                if folder == "valid":
                    background_files = list(self.backgrounds_dir2.iterdir())
                else:
                    background_files = list(self.backgrounds_dir.iterdir())
                images_dir = self.base_output_dir / folder / "images"
                if not images_dir.exists():
                    continue
                
                for file_path in images_dir.iterdir():
                    if file_path.is_file():
                        print(f"ADDING BACKGROUND TO {file_path.name}...".upper())
                        
                        background_file = random.choice(background_files)
                        bg_path = background_file
                        
                        add_background_to_foreground(
                            background_path=str(bg_path),
                            foreground_path=str(file_path),
                            output_image_path=str(file_path),
                        )
            
            print("ADDED BACKGROUNDS TO PART IMAGES.".upper())
    
    def generate_yaml_config(self) -> None:
        """Generate YAML configuration file."""
        try:
            generate_yaml(
                input_folder=str(self.raw_dir),
                output_yaml_path=str(self.base_output_dir / 'data.yaml'),
                train_images_path=str(self.base_output_dir / 'train' / 'images'),
                val_images_path=str(self.base_output_dir / 'valid' / 'images'),
                serials_path='/home/apsu/FieldTest/serials.txt'
            )
            print("GENERATED YAML FILE.".upper())
            
        except Exception as e:
            print(f"Error generating YAML config: {e}")
            raise
    



# --- Main execution block ---
if __name__ == "__main__":
    start_time = time.time()
    try:
        processor = DatasetProcessor()
        
        # Ensure output directory exists
        processor.base_output_dir.mkdir(parents=True, exist_ok=True)
        
        #Execute pipeline steps
        processor.download_part_images()
        processor.download_background_images()
        processor.resize_images()
        processor.convert_backgrounds_to_png()
        processor.remove_backgrounds_from_parts()
        processor.annotate_dataset()
        processor.make_images_transparent()
        processor.augment_dataset()
        processor.convert_parts_to_png()
        processor.resize_backgrounds_again()
        processor.add_backgrounds_to_parts()
        processor.generate_yaml_config()
        
        print("DATASET PROCESSING COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        print(f"Application failed: {e}")
        exit(1)
    finally:
        total_time = time.time() - start_time
        print(f"Total time elapsed: {total_time} seconds or {total_time / 60} minutes.")
