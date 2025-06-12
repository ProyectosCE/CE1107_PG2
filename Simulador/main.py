from core.processor import Processor

print("\n==== SIMULACIÓN COMPLETA: RISC-V 5 ETAPAS ====\n")

program = [
    "addi x2, x0, 4",        # x2 = 4
    "addi x3, x0, 1234",     # x3 = 1234
    "sw x3, 0(x2)",          # mem[4] = 1234
    "lw x1, 0(x2)",          # x1 = mem[4]
    "add x5, x1, x3"         # x5 = x1 + x3 = 1234 + 1234 = 2468
]

cpu = Processor()
cpu.load_program(program)
cpu.run()

# Imprimir resultado final de x5
print(f"\n x5 final = {cpu.registers.read('x5')}")
