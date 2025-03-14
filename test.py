import re
import csv

headers = [
    'device_type',          # 设备类型(英文名)
    'device_class_code',    # 设备类型编号(0c80等)
    'device_name',          # 设备名称
    'device_vendor_id',     # 设备厂商ID(8086等)
    'device_device_id',     # 设备ID(06a4/3442等)
    'revision',             # 修订版本(02等)
    'subsystem_name',       # 子系统名称
    'subsystem_vendor_id',  # 子系统厂商ID
    'subsystem_device_id'   # 子系统设备ID
]

# 定义正则表达式组件
regex_main = re.compile(
    r'^([^\[\]:]+?)\s*'          # 设备类型 (非贪婪匹配到第一个[或:)
    r'(?:\[([0-9a-fA-F]{4})\])?' # 设备类型编号 (可选)
    r':\s*(.*?)\s*'              # 剩余部分
    r'(\(rev\s+([0-9a-fA-F]{2})\))?' # 修订版本 (可选)
    r'(?:\s*Subsystem:\s*(.*?)\s*\[([0-9a-fA-F]{4}):([0-9a-fA-F]{4})\])?', # 子系统信息 (可选)
    re.IGNORECASE
)

regex_device_id = re.compile(
    r'^(.*?)\s+'                # 设备名称 (非贪婪匹配)
    r'(?:\[([0-9a-fA-F]{4}):'  # 厂商ID (可选)
    r'([0-9a-fA-F]{4})\]|'     # 设备ID (格式1)
    r'([0-9a-fA-F]{4}))'       # 设备ID (格式2)
)

def parse_line(line):
    """解析单行PCI设备信息"""
    main_match = regex_main.match(line)
    if not main_match:
        return None
    
    # 基础信息解析
    device_type = main_match.group(1).strip()
    device_class = (main_match.group(2) or '').lower()
    revision = (main_match.group(5) or '').lower()
    print()
    print("Type,Class,Rev:",device_type,device_class,revision)
    # 解析设备名称和ID
    device_info = main_match.group(3)
    print(device_info)
    id_match = regex_device_id.match(device_info)
    print(id_match)
    if not id_match:
        return None
    
    device_name = id_match.group(1).strip()
    vendor_id = (id_match.group(2) or '').lower()
    device_id = id_match.group(3) or id_match.group(4) or ''
    device_id = device_id.lower()
    
    # 子系统信息
    subsystem_name = (main_match.group(6) or '').strip()
    subsys_vendor = (main_match.group(7) or '').lower()
    subsys_device = (main_match.group(8) or '').lower()

    return {
        'device_type': device_type,
        'device_class_code': device_class,
        'device_name': device_name,
        'device_vendor_id': vendor_id,
        'device_device_id': device_id,
        'revision': revision,
        'subsystem_name': subsystem_name,
        'subsystem_vendor_id': subsys_vendor,
        'subsystem_device_id': subsys_device
    }

def process_pci_info(pci_devinfo_list):
    """处理PCI信息列表"""
    valid_data = []
    error_lines = []
    
    for idx, line in enumerate(pci_devinfo_list):
        line = line.strip()
        if not line:
            continue
        
        parsed = parse_line(line)
        if parsed:
            valid_data.append(parsed)
        else:
            error_lines.append(f"Line {idx+1}: {line}")
    
    # 写入CSV
    with open('pci_devices.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(valid_data)
    
    # 记录错误信息
    if error_lines:
        with open('parse_errors.log', 'w', encoding="utf-8") as f:
            f.write("无法解析的行：\n")
            f.write("\n".join(error_lines))

# 示例使用
if __name__ == "__main__":
    sample_data = [
        "Serial bus controller [0c80]: Intel Corporation Comet Lake PCH SPI Controller [8086:06a4] Subsystem: CLEVO/KAPOK Computer Device [1558:8535]",
        "System peripheral: Intel Corporation Device 3442",
        "Host bridge [0600]: Intel Corporation 10th Gen Core Processor Host Bridge/DRAM Registers [8086:9b54] (rev 02) Subsystem: CLEVO/KAPOK Computer Device [1558:8535]",
        "PCI bridge: Intel Corporation Device 490f"
    ]
    
    process_pci_info(sample_data)