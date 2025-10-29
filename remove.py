import os
def remove(folder_path):
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        # Skip directories
        if os.path.isdir(full_path):
            continue

        # Skip files that already end with .jpg
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.png') or filename.lower().endswith('.webp') or filename.lower().endswith('.jpeg'):
            continue

        else:
            os.remove(full_path)


remove("/home/apsu/FuturisticBGS (Copy)")