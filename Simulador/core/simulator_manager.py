"""
SimulatorManager: ejecuta múltiples versiones del procesador RISC-V en paralelo
para comparar sus resultados (básico, sin hazards, completo).
"""

import copy
from core.processor import Processor
from core.processor_basic import ProcessorBasic
from core.processor_no_hazards import ProcessorNoHazards
from core.processor_no_predictor import ProcessorNoPredictor
from InOut.metrics import Metrics

class SimulatorManager:
    def __init__(self, program_lines: list[str]):
        self.program_lines = program_lines

        # Inicializar procesadores
        self.cpu_full = Processor()
        self.cpu_basic = ProcessorBasic()
        self.cpu_no_hazards = ProcessorNoHazards()
        self.cpu_no_predictor = ProcessorNoPredictor()

        # Métricas
        self.metrics_full = Metrics(name="Processor Completo")
        self.metrics_basic = Metrics(name="Processor Básico")
        self.metrics_no_hazards = Metrics(name="Processor Sin Hazards")

    def load_and_run(self, modo="full", delay_seg=1.0):
        # Parsear y cargar en todos los procesadores
        self.cpu_full.load_program(self.program_lines)
        self.cpu_basic.load_program(copy.deepcopy(self.program_lines))
        self.cpu_no_hazards.load_program(copy.deepcopy(self.program_lines))
        self.cpu_no_predictor.load_program(copy.deepcopy(self.program_lines))

        # Ejecutar cada uno
        print("\n=== Ejecutando procesador completo ===")
        self.cpu_full.run(modo=modo, delay_seg=delay_seg)

        print("\n=== Ejecutando procesador básico (sin hazards ni predicción) ===")
        self.cpu_basic.run(modo=modo, delay_seg=delay_seg)

        print("\n=== Ejecutando procesador sin unidad de hazards (con forwarding) ===")
        self.cpu_no_hazards.run(modo=modo, delay_seg=delay_seg)

        print("\n=== Ejecutando procesador sin unidad de predicción (con hazards) ===")
        self.cpu_no_predictor.run(modo=modo, delay_seg=delay_seg)

        print("\n=== Comparación completada ===")
