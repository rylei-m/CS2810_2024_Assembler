def assembler():
    pass
# -------------------------------------------------------------------
# step 1

def preprocess(lines):
    preprocessed = []
    for line in lines:
        line = line.split("#")[0].strip()
        if line:
            preprocessed.append(line)
    return preprocessed

# -------------------------------------------------------------------
# step 2

def build_data_table(lines):
    data_table = {}
    data_list = []
    new_lines = []
    data_section = False

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
                data_table[label] = len(data_list)
                data_list.append(value)
        else:
            new_lines.append(line)

    return data_table, data_list, new_lines

# -------------------------------------------------------------------
# step 3

def build_label_table(lines):
    label_table = {}
    new_lines = []
    line_num = 0

    for line in lines:
        if ':' in line:
            label = line.split(':')[0]
            label_table[label] = line_num
        else:
            new_lines.append(line)
            line_num += 1

    return label_table, new_lines

# -------------------------------------------------------------------
#Step 4

def register_to_binary(register):
    reg_num = int(register[1:])
    return f"{reg_num:03b}"

def dec_to_bin(num, bits):
    if num < 0:
        return f"{(1 << bits) + num:0{bits}b}"
    return f"{num:0{bits}b}"

def encode_instruction(line_num, instruction, label_table, data_table):
    parts = instruction.replace(",", " ").split()
    opcode_map = {
        "add": "0000", "sub": "0000", "and": "0000", "or": "0000", "slt": "0000",
        "addi": "0101", "beq": "0011", "bne": "0110", "lw": "0001", "sw": "0010",
        "j": "0100", "jr": "0111", "jal": "1000", "display": "1111"
    }
    funct_map = {
        "add": "010", "sub": "110", "and": "000", "or": "001", "slt": "111"
    }

    opcode = opcode_map.get(parts[0], None)
    if opcode is None:
        raise ValueError(f"Unsupported instruction: {parts[0]} at line {line_num}")

    if parts[0] in ["add", "sub", "and", "or", "slt"]:
        rd = register_to_binary(parts[1].rstrip(","))
        rs = register_to_binary(parts[2].rstrip(","))
        rt = register_to_binary(parts[3])
        funct = funct_map[parts[0]]
        return f"{opcode} {rs} {rt} {rd} {funct}"

    elif parts[0] in ["addi", "beq", "bne", "lw", "sw"]:
        rt = register_to_binary(parts[1])
        if "(" in parts[2]:
            offset, base = parts[2].split("(")
            offset = int(offset)
            base = base.rstrip(")")
            rs = register_to_binary(base)
            immediate = dec_to_bin(offset, 6)
        elif parts[0] in ["beq", "bne"] and parts[3] in label_table:
            rs = register_to_binary(parts[2])
            immediate = label_table[parts[3]] - line_num - 1
            immediate = dec_to_bin(immediate, 6)
        elif parts[2] in data_table:  # lw/sw with label
            rs = register_to_binary("R0")
            offset = data_table[parts[2]]
            immediate = dec_to_bin(offset, 6)
        else:
            rs = register_to_binary(parts[2])
            immediate = dec_to_bin(int(parts[3]), 6)

        return f"{opcode} {rs} {rt} {immediate}"

    elif parts[0] in ["j", "jal"]:
        address = label_table[parts[1]]
        immediate = dec_to_bin(address, 12)
        return f"{opcode} {immediate}"

    elif parts[0] == "jr":
        rs = register_to_binary(parts[1])
        return f"{opcode} {rs} 000 000000"

    elif parts[0] == "display":
        return f"{opcode} 000 000 000000"

    else:
        raise ValueError(f"Unsupported instruction format: {instruction}")


def encode_program(processed_program, label_table, data_table):
    binary_instructions = []
    for i, instruction in enumerate(processed_program):
        if instruction.strip().endswith(":") or instruction.strip() in [".data", ".text"]:
            continue
        binary_instruction = encode_instruction(i, instruction, label_table, data_table)
        binary_instructions.append(binary_instruction)
    return binary_instructions

# -------------------------------------------------------------------
#Step 5

def binary_to_hex(binary_instructions):
    return [f"{int(b, 2):08x}" for b in binary_instructions]


def post_process(binary_instructions):
    hex_instructions = [f"{int(b.replace(' ', ''), 2):04x}" for b in binary_instructions]
    return hex_instructions


def write_output(hex_instructions, data_list):
    with open("program.hex", "w") as outfile:
        outfile.write("v3.0 hex words addressed\n00: ")
        outfile.write(" ".join(hex_instructions) + "\n")

    with open("data.hex", "w") as outfile:
        outfile.write("v3.0 hex words addressed\n00: ")
        outfile.write(" ".join([f"{d:04x}" for d in data_list]) + "\n")

def write_data_output(data_list):
    with open("data.hex", "w") as outfile:
        outfile.write("v3.0 hex words addressed\n00: ")
        outfile.write(" ".join([f"{d:04x}" for d in data_list]) + "\n")

def write_program_output(hex_instructions):
    with open("program.hex", "w") as outfile:
        outfile.write("v3.0 hex words addressed\n00: ")
        outfile.write(" ".join(hex_instructions) + "\n")
