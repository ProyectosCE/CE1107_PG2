import os
from InOut.program_loader import ProgramLoader
from InOut.parser import Parser
from core.simulator_manager import SimulatorManager

# Obtener la ruta absoluta al archivo programa.s
current_dir = os.path.dirname(__file__)
program_path = os.path.join(current_dir, "programa.s")

# Cargar y parsear el programa fuente
loader = ProgramLoader()
parser = Parser()

program_lines = loader.load_program(program_path)
instructions = parser.parse(program_lines)

# Selección de modo de ejecución
print("Seleccione el modo de ejecución:")
print("  1. full  (ejecución inmediata)")
print("  2. step  (paso a paso)")
print("  3. delay (con retardo entre ciclos)")
modo_op = input("Modo [1/2/3]: ").strip()
if modo_op == "2":
    modo = "step"
    delay_seg = 1.0
elif modo_op == "3":
    modo = "delay"
    try:
        delay_seg = float(input("Ingrese el delay entre ciclos en segundos (ej: 0.5): ").strip())
    except Exception:
        delay_seg = 1.0
else:
    modo = "full"
    delay_seg = 1.0

# Preparar la simulación con los tres procesadores
manager = SimulatorManager([str(instr.raw_text) for instr in instructions])
manager.load_and_run(modo=modo, delay_seg=delay_seg)
