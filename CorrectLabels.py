import os

def replace_first_three_if_dot(folder_path):
        for filename in os.listdir(folder_path):

            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                if len(line) >= 3 and line[1] == '.':
                    new_line = line[0] + line[3:]
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)


# Example usage:
replace_first_three_if_dot('/home/apsu/FieldTest/DS2/train/labels')
replace_first_three_if_dot('/home/apsu/FieldTest/DS2/valid/labels')