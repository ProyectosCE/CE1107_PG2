import os
from InOut.program_loader import ProgramLoader
from InOut.parser import Parser
from core.simulator_manager import SimulatorManager

# Obtener la ruta absoluta del archivo fuente
current_dir = os.path.dirname(__file__)
program_path = os.path.join(current_dir, "programa.s")

# Cargar y parsear el programa
loader = ProgramLoader()
parser = Parser()

program_lines = loader.load_program(program_path)
parsed_instructions = parser.parse(program_lines)
instruction_texts = [instr.raw_text for instr in parsed_instructions]

# Ejecutar ambos procesadores simultáneamente
manager = SimulatorManager(instruction_texts)
manager.load_and_run()
