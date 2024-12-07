import os

from assembler import build_data_table, build_label_table, encode_program, preprocess, post_process, write_output, \
    write_program_output, write_data_output


def main():
    # Defining the assembly file to read from
    folder = "Files"
    filename = os.path.join(folder, "test12.asm")

    if not os.path.exists(filename):
        print(f"ERROR: The file {filename} does not exist.")
        return

    # Read all lines from the assembly file, and store them in a list
    with open(filename, "r") as infile:
        lines = infile.readlines()

    # Step 1: Preprocess the lines to remove comments and whitespace
    lines = preprocess(lines)
    print("STEP 1: Preprocess the lines to remove comments and whitespace")
    print("Preprocessed Lines:", lines)
    print(" ")

    # Step 2: Use the preprocessed program to build data table
    data_table, data_list, processed_program = build_data_table(lines)
    print("STEP 2: Use the preprocessed program to build data table")
    print("Data Table:", data_table)
    print("Data List:", data_list)
    print("Processed Program:", processed_program)
    print(" ")

    # Step 3: Build a label table and strip out the labels from the code
    label_table, instructions = build_label_table(lines)
    print("STEP 3: Build a label table and strip out the labels from the code")
    print("Label Table:", label_table)
    print("Processed Instructions:", instructions)
    print(" ")

    # Step 4: Encode the program into a list of binary strings
    binary_instructions = encode_program(instructions, label_table, data_table)
    print("STEP 4: Encode the program into a list of binary strings")
    print("Binary Instructions:")
    for binary in binary_instructions:
        print(binary)
    print(" ")

    # Step 5: Convert the strings to hexadecimal and write them to a file
    # hex_program = post_process(encoded_program)
    # with open("output.hex", "w") as outfile:
    # outfile.write("v3.0 hex words addressed\n00: ")
    # outfile.writelines(hex_program)
    # hex_instructions = post_process(binary_instructions)
    # write_output(hex_instructions, data_list)
    hex_instructions = post_process(binary_instructions)
    print("STEP 5: Hex Instructions:")
    print(hex_instructions)

    # Write the hex instructions to the output file
    write_program_output(hex_instructions)
    write_data_output(data_list)
    print("Hex files written: program.hex and data.hex")

    # Step 6: Convert the data list to hexadecimal and write it to a file
    # with open("data.hex", "w") as outfile:
    # outfile.write("v3.0 hex words addressed\n00: ")
    # outfile.writelines([f"{d:04x} " for d in data_list])

if __name__ == "__main__":
    main()