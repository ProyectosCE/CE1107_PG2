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

# Preparar la simulación con los tres procesadores
manager = SimulatorManager([str(instr.raw_text) for instr in instructions])
manager.load_and_run()
