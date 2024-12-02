.data
screenStart: 16384    # 0x4000
screenEnd: 24576      # 0x6000

.text
j main


main:

lw R1, screenStart
lw R2, screenEnd
addi R3, R3, 0  # R3 will hold the color

drawLoop:
    beq R1, R2, drawEnd

    # Draw pixel to current address
    sw R3, 0(R1)

    # Add one to the address and color and jump to top
    addi R1, R1, 1
    addi R3, R3, 9

    # Update the screen every pixel we draw
    display

    j drawLoop



drawEnd:
    # Reset the address pointer to the start of the screen
    lw R1, screenStart
    j drawLoop