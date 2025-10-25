import os
from openpyxl import load_workbook

wb = load_workbook(filename="DC_Filler_List.xlsx", read_only=True)
ws = wb["DC_Filler"]
dc_Filler = {}
for row in ws.values:
    w,x,y,z = row
    dc_Filler[w] = (x, y, z)

for root, dirs, files in os.walk(r"E:\Videos\Detective Conan"):
    for file_name in files:
        src = root + "\\" + file_name
        num = int(file_name[:3])
        x, y, z = dc_Filler[num]
        x = str.replace(x, ":", "_")
        x = str.replace(x, "\"", "_")
        dst = root + "\\" + "Detective Conan - " + file_name[:-4] + " - " + x
        if y == "FILLER":
            dst = dst + " (Filler)"
        dst = dst + file_name[-4:]
        os.rename(src, dst)