import os
from InOut.program_loader import ProgramLoader
from InOut.parser import Parser
from core.simulator_manager import SimulatorManager

from gui.riscv_sim import RiscVSimulatorApp

current_dir = os.path.dirname(__file__)
program_path = os.path.join(current_dir, "programa.s")

# Cargar y parsear el programa fuente
loader = ProgramLoader()
parser = Parser()

program_lines = loader.load_program(program_path)
instructions = parser.parse(program_lines)




if __name__ == "__main__":
    app = RiscVSimulatorApp()
    app.mainloop()