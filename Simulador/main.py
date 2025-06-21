# main.py

from core.processor import Processor

print("\n==== SIMULACIÓN DE CONTROL UNIT COMPLETO ====\n")

program = [
    "addi x1, x0, 10",   
    "addi x2, x0, 20",    
    "add x3, x1, x2",     
    "sw x3, 0(x0)",       
    "lw x4, 0(x0)",       
    "beq x1, x2, 8",      
    "add x5, x0, x0",     
    "jal x6, 4",          
    "add x7, x0, x0"      
]

cpu = Processor()

# No es necesario precargar registros

cpu.load_program(program)
cpu.run()

# Mostrar resultados
print("\n Resultado final:")
print(f"x1 = {cpu.registers.read('x1')}")  # Esperado: 10
print(f"x2 = {cpu.registers.read('x2')}")  # Esperado: 20
print(f"x3 = {cpu.registers.read('x3')}")  # Esperado: 30
print(f"x4 = {cpu.registers.read('x4')}")  # Esperado: 30 (cargado de memoria)
print(f"x5 = {cpu.registers.read('x5')}")  # Esperado: 0
print(f"x6 = {cpu.registers.read('x6')}")  # Esperado: dirección de retorno (PC + 4)
print(f"x7 = {cpu.registers.read('x7')}")  # Esperado: 0 (instrucción fue saltada)
print(f"Mem[0] = {cpu.data_mem.load_word(0)}")  # Esperado: 30
