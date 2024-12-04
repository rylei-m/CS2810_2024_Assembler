def assembler():
    pass

def preprocess_lines(lines):
    preprocessed = []
    for line in lines:
        line = line.split("#")[0].strip()
        if line:
            preprocessed.append(line)
    return preprocessed
