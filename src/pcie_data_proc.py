# -*- coding: utf-8 -*-

import csv

pci_csv_filename = "table_pcie.csv"
pci_devinfo_list = list()

with open(pci_csv_filename, encoding="utf-8") as file:
    table = csv.DictReader(file)
    for line in table:
        if line.get("Rev") == "-":
            line["Rev"] = "00"
        
        vidpid = line.get("VID_PID")
        name = line.get("CurrentName")
        name = name.strip()
        
        if len(vidpid) <= 4 :
            vidprefix = "0000:"
            if name == "[Intel]" :
                vidprefix = "8086:"
            if name == "[AMD]" :
                vidprefix = "1022:"
            if name == 'Loongson Technology LLC Device':
                line["CommonName"] = "[Loongson]"
                vidprefix = "0014:"
            
            if vidprefix == "0000:":
                print("NO AVAIL VID")
            else:
                line["VID_PID"] = vidprefix + vidpid
                
        print(list(line.values()))
        pci_devinfo_list.append(list(line.values()))
        
    pass

seen = set()
processed_pci_devinfo_list = []
for row in pci_devinfo_list:
    row_tuple = tuple(row)
    if row_tuple not in seen:
        seen.add(row_tuple)
        processed_pci_devinfo_list.append(row)

header = list(line)

pci_csv_filename = "table_pcie.csv"

# 写入CSV文件（自动处理含逗号的字段）
with open(f"proc_{pci_csv_filename}", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(header)
    writer.writerows(processed_pci_devinfo_list)