    addi x1, x0, 10      # x1 = 10 (contador)
    addi x2, x0, 0       # x2 = 0  (acumulador)
    addi x3, x0, 4       # x3 = 4  (incremento de 4 para direcciones alineadas)
    addi x4, x0, 20      # x4 = 20 (límite para comparación)
    addi x5, x0, 0       # x5 = 0  (dirección base memoria)

loop:
    lw   x6, 0(x5)       # x6 = mem[x5] (RAW hazard con x5, fuerza stall si no hay forwarding)
    add  x7, x6, x2      # x7 = x6 + x2 (RAW hazard con x6)
    sw   x7, 0(x5)       # mem[x5] = x7 (RAW hazard con x5)
    add  x5, x5, x3      # x5 += 4 (dirección memoria, RAW)
    sub  x8, x4, x1      # x8 = x4 - x1 (RAW con x1)
    slt  x9, x2, x4      # x9 = (x2 < x4) ? 1 : 0
    andi x10, x2, 3      # x10 = x2 & 3 (prueba lógica inmediata)
    or   x11, x2, x8     # x11 = x2 | x8 (prueba lógica)
    sll  x12, x2, x3     # x12 = x2 << 4 (prueba shift)
    srl  x13, x2, x3     # x13 = x2 >> 4 (prueba shift)
    beq  x9, x0, next    # si x2 >= x4, saltar a next (control hazard)

    addi x2, x2, 1       # x2++
    addi x1, x1, -1      # x1--
    bne  x1, x0, loop    # si x1 != 0, repetir loop (control hazard)

next:
    addi x14, x0, 42     # x14 = 42 (fin, instrucción visible)
    jal  x0, end         # salto incondicional a end

    addi x15, x0, 99     # (no se ejecuta, prueba de flush)

end:
    addi x16, x0, 7      # x16 = 7 (marca de fin)
