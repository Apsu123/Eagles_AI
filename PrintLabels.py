import os

def print_all_text_files(folder_path):
    for filename in os.listdir(folder_path):

        print(filename)
        if "0_" or "1_" in filename.lower():
            file_path = os.path.join(folder_path, filename)
            print(f"--- {filename} ---")
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f.read())

# Example usage:
#
print_all_text_files('/home/apsu/Predict/Test/valid/labels')
print("ÖÖÖÖÖÖÖÖÖÖÖÖÖÖÖ")
print_all_text_files("/home/apsu/FieldTest/DS4/valid/labels")