# main.py

from core.processor import Processor

print("\n SIMULACIÓN RISC-V: IF → ID → EX \n")

program = [
    "add x1, x2, x3",
    "sub x4, x1, x5",
    "addi x6, x0, 10",
    "beq x2, x3, 8",
    "and x7, x1, x2"
]

initial_regs = {
    "x2": 10,
    "x3": 5,
    "x5": 3
}

cpu = Processor()
cpu.load_program(program)
cpu.preload_registers(initial_regs)
cpu.run()
