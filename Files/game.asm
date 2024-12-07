.data
screenStart: 16384
screenEnd: 24576
ballColor: 65535
backgroundColor: 0
rowShift: 128
xVelocity: 1
yVelocity: 1
ballPos: 16704

.text
main:
    j main

    drawBall:
        sw R1, 0(R2)
        jr R7

    clearBall:
        sw R1, 0(R2)
        jr R7

    moveBall:
        lw R1, xVelocity
        lw R2, ballPos
        add R2, R2, R1
        lw R3, rowShift
        lw R4, yVelocity
        bne R4, R0, updateY

    updateY:
        add R2, R2, R4

    checkCollision:
        lw R3, screenStart
