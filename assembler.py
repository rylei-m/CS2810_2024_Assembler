def assembler():
    pass

def preprocess_lines(lines):
    preprocessed = []
    for line in lines:
        line = line.split("#")[0].strip()
        if line:
            preprocessed.append(line)
    return preprocessed

def build_data_table(lines):
    data_table = {}
    data_list = []
    new_lines = []
    data_section = False
    memory_address = 0

    for line in lines:
        if line == ".data":
            data_section = True
            continue
        elif line == ".text":
            data_section = False
            continue

        if data_section:
            if ":" in line:
                label, value = line.split(":")
                label = label.strip()
                value = int(value.strip())
                data_table[label] = memory_address
                data_list.append(value)
                memory_address += 1
        else:
            new_lines.append(line)

    return data_table, data_list, new_lines
