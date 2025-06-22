import os
from InOut.program_loader import ProgramLoader
from InOut.parser import Parser
from core.processor import Processor

from gui.riscv_sim import RiscVSimulatorApp

# Obtener la ruta absoluta al archivo desde el propio main.py
current_dir = os.path.dirname(__file__)
program_path = os.path.join(current_dir, "programa.s")

loader = ProgramLoader()
parser = Parser()
cpu = Processor()

program_lines = loader.load_program(program_path)
instructions = parser.parse(program_lines)

cpu.load_program([str(instr.raw_text) for instr in instructions])
cpu.run()


if __name__ == "__main__":
    app = RiscVSimulatorApp()
    app.mainloop()