# 去除表格中的无用信息(如kernel module等)

import csv

usb_csv_filename = "usb_hwdata_feb20.csv"

usb_devinfo_list = []
usb_devinfo_extradata = []

with open(usb_csv_filename, encoding="utf-8") as file:
    table = csv.DictReader(file)
    for row in table:
        time_str = row["Time"]
        
        info_str = row["Info_USB"]
        info_lines = info_str.splitlines()

        for line in info_lines:
            stripped_line = line.strip()
            elements = stripped_line.split(" ")
            if ("Foundation" in elements) or ("$" in elements):
                # print("Ignore")
                pass
            else:
                if ("Bus" in elements) and ("Device" in elements):
                    stripped_line = stripped_line[23:]
                    # Vendor ID, Product ID, Name
                    vidpid_name = stripped_line.split(sep=" ", maxsplit=1)
                    vidpid = vidpid_name[0].upper().split(":")
                    name = "[UNKNOWN_DEVICE_NAME]" if len(vidpid_name) == 1 else vidpid_name[1]
                    device_info = [vidpid[0], vidpid[1], name]
                    usb_devinfo_list.append(device_info)
                    pass
                else:
                    extra_data_note = ( f"[EXTRA_DATA @ {time_str.split(" ")[0]}] {stripped_line}" )
                    usb_devinfo_extradata.append([extra_data_note])
                    
print(usb_devinfo_list)
print(usb_devinfo_extradata)

seen = set()
processed_usb_devinfo_list = []
for row in usb_devinfo_list:
    row_tuple = tuple(row)
    if row_tuple not in seen:
        seen.add(row_tuple)
        processed_usb_devinfo_list.append(row)

header = ["VendorID", "ProductID", "DeviceName"]

# 写入CSV文件（自动处理含逗号的字段）
with open(f"processed_{usb_csv_filename}", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    # writer.writerow(header)  # 先写入表头
    writer.writerows(processed_usb_devinfo_list)   # 再写入数据行

with open(f"processed_extradata_{usb_csv_filename}", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerows(usb_devinfo_extradata) 
