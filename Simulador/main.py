from core.processor import Processor

print("\n SIMULACIÓN CON VARIOS SALTOS (beq) \n")

program = [
    "beq x1, x2, 8",     # PC=0 → no tomado (x1 ≠ x2) → puede provocar flush
    "add x3, x0, x0",    # PC=4 → ejecuta después del flush
    "beq x5, x5, 8",     # PC=8 → sí se toma (x5 == x5) → salta a PC=16
    "add x6, x0, x0",    # PC=12 → se salta si el branch es tomado
    "add x7, x0, x0"     # PC=16 → ejecuta después de salto tomado
]

# Inicializar procesador
cpu = Processor()

# Precargar registros
cpu.preload_registers({
    "x1": 10,   # x1 ≠ x2 → no se toma
    "x2": 20,
    "x5": 42    # x5 == x5 → sí se toma
})

# Cargar instrucciones
cpu.load_program(program)

# Ejecutar simulación
cpu.run()

# Mostrar resultados
print("\n Resultado final:")
print(f"x3 = {cpu.registers.read('x3')}")
print(f"x6 = {cpu.registers.read('x6')}")
print(f"x7 = {cpu.registers.read('x7')}")
