def rewrite_first_char(input_file, output_file=None, replacement_char='*'):
    """
    Rewrites the first character of each line in a file.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to save the modified file. If None, overwrites input_file.
        replacement_char (str): Character to replace the first character of each line.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        modified_lines = [
            (replacement_char + line[1:]) if line else '\n'
            for line in lines
        ]

        target_file = output_file if output_file else input_file

        with open(target_file, 'w', encoding='utf-8') as f:
            f.writelines(modified_lines)

        print(f"✅ File processed successfully.")
        print(f"➡ Output written to: {target_file}")
    except FileNotFoundError:
        print(f"❌ Error: File not found - {input_file}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


# Run the function with your desired settings
if __name__ == "__main__":
    # 👇 Set your file paths and replacement character here
    input_file_path = "/home/apsu/LegoDetect/TestReplace.txt"
    output_file_path = None  # Set to None to overwrite input file
    replacement_character = "#"

    rewrite_first_char(input_file_path, output_file_path, replacement_character)
