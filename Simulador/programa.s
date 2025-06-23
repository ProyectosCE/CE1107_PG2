# Prueba integral de instrucciones y dependencias para todos los procesadores

    addi x1, x0, 10      # x1 = 10 (contador)
    addi x2, x0, 0       # x2 = 0  (acumulador)
    addi x3, x0, 4       # x3 = 4  (incremento de 4 para direcciones alineadas)
    addi x4, x0, 20      # x4 = 20 (límite para comparación)
    addi x5, x0, 0       # x5 = 0  (dirección base memoria)

loop:
    add  x2, x2, x3      # x2 += 4 (RAW con x2)
    sub  x6, x4, x1      # x6 = x4 - x1 (RAW con x1)
    slt  x7, x2, x4      # x7 = (x2 < x4) ? 1 : 0
    andi x8, x2, 3       # x8 = x2 & 3 (prueba lógica inmediata)
    or   x9, x2, x6      # x9 = x2 | x6 (prueba lógica)
    sll  x10, x2, x3     # x10 = x2 << 4 (prueba shift)
    srl  x11, x2, x3     # x11 = x2 >> 4 (prueba shift)
    add  x5, x5, x3      # x5 += 4 (dirección memoria, RAW)
    sw   x2, 0(x5)       # mem[x5] = x2 (RAW hazard con x5)
    lw   x12, 0(x5)      # x12 = mem[x5] (RAW hazard con x5)
    beq  x7, x0, next    # si x2 >= x4, saltar a next

    addi x1, x1, -1      # x1--
    bne  x1, x0, loop    # si x1 != 0, repetir loop

next:
    addi x13, x0, 42     # x13 = 42 (fin, instrucción visible)
    jal  x0, end         # salto incondicional a end

    addi x14, x0, 99     # (no se ejecuta, prueba de flush)

end:
    addi x15, x0, 7      # x15 = 7 (marca de fin)
