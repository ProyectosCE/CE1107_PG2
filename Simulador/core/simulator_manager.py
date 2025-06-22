"""
SimulatorManager: ejecuta dos versiones del procesador RISC-V en paralelo
para comparar sus resultados (básico vs completo).
"""

import copy
from core.processor import Processor
from core.processor_basic import ProcessorBasic
from InOut.metrics import Metrics

class SimulatorManager:
    def __init__(self, program_lines: list[str]):
        self.program_lines = program_lines

        # Inicializar procesadores
        self.cpu_full = Processor()
        self.cpu_basic = ProcessorBasic()

        # Métricas
        self.metrics_full = Metrics(name="Processor Completo")
        self.metrics_basic = Metrics(name="Processor Básico")

    def load_and_run(self):
        # Parsear y cargar en ambos procesadores
        self.cpu_full.load_program(self.program_lines)
        self.cpu_basic.load_program(copy.deepcopy(self.program_lines))

        # Ejecutar ambos
        print("\n=== Ejecutando procesador completo ===")
        self.cpu_full.run()

        print("\n=== Ejecutando procesador básico (sin hazards ni predicción) ===")
        self.cpu_basic.run()

        print("\n=== Comparación completada ===")
