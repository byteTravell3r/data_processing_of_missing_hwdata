# 去除表格中的无用信息(如kernel module等)

import csv, re

pci_csv_filename = "pcie_hwdata_feb20.csv"

pci_devinfo_list_1st = []
pci_devinfo_extradata = []


def match_device_position(input_text):
    pattern_1 = re.compile(r"[A-Za-z0-9]+:[A-Za-z0-9]+\.[A-Za-z0-9]+", re.IGNORECASE)
    pattern_2 = re.compile(
        r"[A-Za-z0-9]+:[A-Za-z0-9]+:[A-Za-z0-9]+\.[A-Za-z0-9]+", re.IGNORECASE
    )
    result_1 = pattern_1.match(input_text)
    result_2 = pattern_2.match(input_text)

    if result_1 != None:
        return 8
    elif result_2 != None:
        return 13
    else:
        return 0


with open(pci_csv_filename, encoding="utf-8") as file:
    table = csv.DictReader(file)

    info_of_one_device = ""

    for row in table:
        time_str = row["Time"]

        info_str = row["Info_PCI"]
        info_lines = info_str.splitlines()

        for line in info_lines:
            stripped_line = line.strip()
            elements = stripped_line.split(" ")

            # 判断此行是否为有用信息
            if (
                (stripped_line == "")
                or ("$" in elements)
                or ("modules:" in elements)
                or ("use:" in elements)
                or ("Flags:" in elements)
                or ("Capabilities:" in elements)
                or ("DeviceName:" in elements)
                or ("Error" in elements)
                or ("Processor" in elements)
                or ("SMBus" in elements)
                or ("DRAM" in elements)
                or ("Thermal" in elements)
                or ("Rembrandt" in elements)
                or ("VanGogh" in elements)
                or ("Phoenix" in elements)
                or ("Comet" in elements)
                or ("Jasper" in elements)
                or ("Alder" in elements)
                or ("Meteor" in elements)
                or ("Raptor" in elements)
                or ("Sunrise" in elements)
                or ("Accelerator" in elements)
            ):
                # print("[IGNORE THIS LINE]")
                pass
            else:
                ret = match_device_position(stripped_line)
                if ret != 0:
                    # print(info_of_one_device)
                    pci_devinfo_list_1st.append(info_of_one_device)
                    info_of_one_device = ""
                    info_of_one_device += stripped_line[ret:]
                else:
                    info_of_one_device += " "
                    info_of_one_device += stripped_line

pci_devinfo_list_2nd = []

for line in pci_devinfo_list_1st:
    linestr = str(line)
    split_str = linestr.split(sep=":",maxsplit=1)
    if len(split_str) != 2:
        pass
    else:
        devicetype_class = split_str[0].split("[")
        devicetype_class[0] = devicetype_class[0].strip()
        if len(devicetype_class) == 2:
            devicetype_class[1] = devicetype_class[1][0:4].upper()
        else:
            devicetype_class.append("-")
        deviceinfo_subsystem = list(split_str[1].partition("Subsystem:"))

        deviceinfo_subsystem[1] = "SUBSYS"
        if deviceinfo_subsystem[2] == "": deviceinfo_subsystem[2] = "-"
        deviceinfo_subsystem[0] = deviceinfo_subsystem[0].strip()
        deviceinfo_subsystem[1] = deviceinfo_subsystem[1].strip()
        
        deviceinfo_rev = list(deviceinfo_subsystem[0].partition("(rev "))
        deviceinfo_rev[0] = deviceinfo_rev[0].strip()
        deviceinfo_rev[1] = "REV"
        if deviceinfo_rev[2] == "":
            deviceinfo_rev[2] = "-"
        else: 
            deviceinfo_rev[2] = deviceinfo_rev[2][0:2]
        deviceinfo_subsystem[2] = deviceinfo_subsystem[2].strip()
        info_of_onedevice = devicetype_class + deviceinfo_rev + [deviceinfo_subsystem[1], deviceinfo_subsystem[2]]
        # info_of_onedevice.remove('REV')
        # info_of_onedevice.remove("SUBSYS")
        pci_devinfo_list_2nd.append(info_of_onedevice)
        
# print(pci_devinfo_list_2nd)

pci_devinfo_list_3rd = []
    
for line in pci_devinfo_list_2nd:
    split_info_of_onedevice = []
    devname_class = []
    # print(line)    
    if line[2].endswith("]"):
        devname_class = list(line[2].rpartition("["))
        devname_class[2] = devname_class[2][0:9]
        devname_class.remove("[")

        pass
    else:
        devname = line[2][:-4]
        classcode = line[2][-4:]
        devname_class.append(devname)
        devname_class.append(classcode)
        pass
    
    split_info_of_onedevice.append(line[0])
    split_info_of_onedevice.append(line[1])
    for element in devname_class:
        split_info_of_onedevice.append(element)
    # split_info_of_onedevice.append(line[3])
    split_info_of_onedevice.append(line[4])
    # split_info_of_onedevice.append(line[5])
    split_info_of_onedevice.append(line[6])
    pci_devinfo_list_3rd.append(split_info_of_onedevice)
    print(split_info_of_onedevice)
    pass

seen = set()
processed_pci_devinfo_list = []
for row in pci_devinfo_list_3rd:
    row_tuple = tuple(row)
    if row_tuple not in seen:
        seen.add(row_tuple)
        processed_pci_devinfo_list.append(row)

header = ["ClassName", "ClassID", "DeviceName", "DeviceID", "DeviceRev", "SubsysInfo", "Extra"]

# 写入CSV文件（自动处理含逗号的字段）
with open(f"processed_{pci_csv_filename}", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(header)
    writer.writerows(processed_pci_devinfo_list)