from core.processor import Processor

print("\n SIMULACIÓN CON DETECCIÓN DE LOAD-USE HAZARD \n")

# Programa de prueba con hazard
program = [
    "lw x1, 0(x2)",          # x1 ← mem[x2]
    "add x3, x1, x4",        # usa x1 inmediatamente → provoca STALL
    "add x5, x1, x6",        # debería avanzar normalmente (forwarding futuro)
    "add x7, x3, x5"         # puede recibir ambos valores previamente procesados
]

# Crear procesador
cpu = Processor()

# Precargar valores en registros
cpu.preload_registers({
    "x2": 4,     # dirección base
    "x4": 10,
    "x6": 20
})

# Precargar memoria
cpu.preload_data_memory({
    4: 100  # mem[4] = 100 → será cargado en x1
})

# Cargar el programa y ejecutar
cpu.load_program(program)
cpu.run()

# Resultado final esperado: x7 = x3 + x5 = (100 + 10) + (100 + 20) = 230
print(f"\n Resultado final x7 = {cpu.registers.read('x7')}")
