from core.processor import Processor

print("\n SIMULACIÓN RISC-V: IF → ID → EX → MEM \n")

program = [
    "addi x2, x0, 4",        # x2 = 4
    "addi x3, x0, 1234",     # x3 = 1234
    "sw x3, 0(x2)",          # mem[4] = 1234
    "lw x1, 0(x2)",          # x1 = mem[4] => 1234
    "add x5, x1, x3"         # x5 = x1 + x3 => 2468
]

cpu = Processor()
cpu.load_program(program)
cpu.preload_registers({})  # se puede setear valores si se quiere
cpu.run()
