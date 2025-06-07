from core.processor import Processor

print("\n==== PRUEBA DE SIMULACIÓN DEL PROCESADOR ====\n")

program = [
    "add x1, x2, x3",
    "sub x4, x5, x6",
    "addi x7, x0, 10",
    "and x8, x1, x2"
]

cpu = Processor()
cpu.load_program(program)
cpu.run()
