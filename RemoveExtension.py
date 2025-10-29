def remove_jpg_extension(filename):
    if filename.lower().endswith('.jpg'):
        return filename[:-4]  # Remove last 4 characters (".jpg")
    return filename


def process_serials(serials_path):
    with open(serials_path, 'r') as file:
        # Loop through each line in the file
        for line_number, line in enumerate(file, start=1):
            # Remove trailing newline characters
            clean_line = line.strip()
            # Example usage
            original_filename = "example.jpg"
            new_filename = remove_jpg_extension(original_filename)
            print(f"Original: {original_filename}")
            print(f"Without .jpg: {new_filename}")


if __name__ == "__main__":
    process_serials('/home/apsu/LegoDetect/serials.txt')
