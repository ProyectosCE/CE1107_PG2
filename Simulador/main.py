import os
from InOut.program_loader import ProgramLoader
from InOut.parser import Parser
from core.processor_basic import ProcessorBasic 

# Obtener la ruta absoluta al archivo desde el propio main.py
current_dir = os.path.dirname(__file__)
program_path = os.path.join(current_dir, "programa.s")

# Cargar programa fuente
loader = ProgramLoader()
parser = Parser()

# Instanciar procesador básico (sin hazards ni predicción)
cpu = ProcessorBasic()

# Leer archivo, parsear e inicializar
program_lines = loader.load_program(program_path)
instructions = parser.parse(program_lines)
cpu.load_program([str(instr.raw_text) for instr in instructions])

# Ejecutar simulación
cpu.run()
