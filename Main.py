import os

from assembler import preprocess_lines, build_data_table, build_label_table


def main():
    # Defining the assembly file to read from
    folder = "Files"
    filename = os.path.join(folder, "test5.asm")

    if not os.path.exists(filename):
        print(f"ERROR: The file {filename} does not exist.")
        return

    # Read all lines from the assembly file, and store them in a list
    with open(filename, "r") as infile:
        lines = infile.readlines()

    # Step 1: Preprocess the lines to remove comments and whitespace
    lines = preprocess_lines(lines)

    print("Preprocessed Lines:", lines)

    # Step 2: Use the preprocessed program to build data table
    data_table, data_list, processed_program = build_data_table(lines)

    print("Data Table:", data_table)
    print("Data List:", data_list)
    print("Processed Program:", processed_program)

    # Step 3: Build a label table and strip out the labels from the code
    label_table, instructions = build_label_table(lines)

    print("Label Table:", label_table)
    print("Processed Instructions:", instructions)

    # Step 4: Encode the program into a list of binary strings
    # encoded_program = encode_program(lines, label_table, data_table)

    # Step 5: Convert the strings to hexadecimal and write them to a file
    # hex_program = post_process(encoded_program)
    # with open("output.hex", "w") as outfile:
    # outfile.write("v3.0 hex words addressed\n00: ")
    # outfile.writelines(hex_program)

    # Step 6: Convert the data list to hexadecimal and write it to a file
    # with open("data.hex", "w") as outfile:
    # outfile.write("v3.0 hex words addressed\n00: ")
    # outfile.writelines([f"{d:04x} " for d in data_list])

if __name__ == "__main__":
    main()