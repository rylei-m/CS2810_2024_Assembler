main:                           # Main program label

    jal     printMessage        # Call the subroutine printMessage

    # More main program code could go here

    jr      R5                 # Return from main (if in a larger system)

printMessage:                   # Subroutine to print a message
    # Code to print the message would go here.
    # This is just a placeholder to demonstrate `jal` and `jr`.

    jr      R7                 # Return from subroutine