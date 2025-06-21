# Programa de prueba
addi x1, x0, 10
addi x2, x1, 5
beq x1, x2, etiqueta
jal x0, etiqueta
etiqueta: add x3, x1, x2
