    addi x1, x0, 5      # x1 = 5
    addi x2, x0, 3      # x2 = 3
    add  x3, x1, x2     # x3 = x1 + x2 = 8
    sw   x3, 0(x0)      # mem[0] = x3
    lw   x4, 0(x0)      # x4 = mem[0] = 8
    beq  x4, x3, match  # salto si x4 == x3
    addi x5, x0, -1     # (no se ejecuta si salto se tomó)
match:
    addi x6, x6, 1      # x6++
    addi x1, x1, -1     # x1--
    beq  x1, x0, end    # si x1 == 0, termina
    jal  x0, match      # saltar a match (loop)
end:
