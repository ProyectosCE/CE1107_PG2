import sys
import os

# Asegurarse de que se puedan importar los módulos internos
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from components.register_file import RegisterFile
from components.memory import Memory
from IO.parser import Parser

print("==== SIMULADOR RISC-V BÁSICO ====\n")

# Programa de ejemplo con etiquetas
program = [
    "start: add x1, x0, x0",        # x1 = 0
    "addi x2, x1, 10",              # x2 = 10
    "loop: beq x2, x0, end",        # if x2 == 0 jump to end
    "addi x2, x2, -1",              # x2 = x2 - 1
    "jal x0, loop",                 # jump to loop
    "end: sw x1, 0(x2)"             # memory[x2] = x1
]

# Parsear instrucciones
parser = Parser()
instructions = parser.parse(program)

print("Instrucciones parseadas:")
for instr in instructions:
    print(instr)

# Crear banco de registros y simular escritura/lectura
rf = RegisterFile()
print("\nEscribiendo valores iniciales en registros...")
rf.write("x1", 5)
rf.write("x2", 16)

print("\n Valores actuales de x1 y x2:")
print(f"x1 = {rf.read('x1')}")
print(f"x2 = {rf.read('x2')}")

# Crear memoria y simular escritura
mem = Memory(size_in_words=32)  # 128 bytes

print("\n Escribiendo valor 999 en dirección 16...")
mem.store_word(16, 999)

print("Leyendo memoria en dirección 16...")
print(f"mem[16] = {mem.load_word(16)}")

print("\n Dump parcial de memoria [0 - 32]:")
mem_dump = mem.dump(0, 32)
for addr, val in mem_dump.items():
    print(f"{addr:04d}: {val}")

# Todo listo
print("\n Simulación terminada.")
