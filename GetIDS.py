import os

IDS_txt = "/home/apsu/FieldTest/serials.txt"

with open(IDS_txt, 'r') as file:
    serials = [line.strip() for line in file if line.strip and "x" not in line.strip() and " " not in line.strip()]


print(serials)