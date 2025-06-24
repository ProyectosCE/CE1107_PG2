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
from InOut.execution_history import ExecutionHistory

class SimulatorManager:
    """
    active_indices: lista de índices de procesadores activos (ej: [0,3])
    0: Básico (sin unidad de riesgos)
    1: Con unidad de riesgos
    2: Con predicción de saltos
    3: Completo (unidad de riesgos + predicción de saltos)
    """
    # --- Agrega la variable de clase para los nombres ---
    CPU_NAMES = [
        "Procesador Básico (sin hazards ni predicción)",
        "Procesador Sin Hazards (con forwarding)",
        "Procesador Sin Predictor (con hazards)",
        "Procesador Completo"
    ]

    def __init__(self, program_lines: list[str], active_indices=None):
        self.program_lines = program_lines
        if active_indices is None:
            active_indices = [0, 3]  # por defecto: básico y completo

        self.active_indices = active_indices

        # Diccionario de procesadores y sus metadatos
        self.cpu_classes = [
            ProcessorBasic,         # 0
            ProcessorNoHazards,     # 1
            ProcessorNoPredictor,   # 2
            Processor               # 3
        ]
        # Cambia a usar la variable de clase
        self.cpu_names = SimulatorManager.CPU_NAMES
        self.cpu_configs = [
            {"Hazards": False, "Predictor": False},
            {"Hazards": False, "Predictor": True},
            {"Hazards": True, "Predictor": False},
            {"Hazards": True, "Predictor": True}
        ]

        # Instanciar solo los procesadores seleccionados
        self.cpus = []
        self.metrics = []
        for idx in self.active_indices:
            cpu = self.cpu_classes[idx]()
            self.cpus.append(cpu)
            self.metrics.append(Metrics(name=self.cpu_names[idx]))

        #Historial de ejecuciones
        self.history = ExecutionHistory(num_procs=len(self.cpus))

    def load_and_run(self, modo="full", delay_seg=1.0):
        # Ejecutar los procesadores seleccionados (asumiendo que ya tienen el programa cargado)
        for i, idx in enumerate(self.active_indices):
            cpu = self.cpus[i]
            print(f"\n=== Ejecutando {self.cpu_names[idx]} ===")
            try:
                cpu.run(modo=modo, delay_seg=delay_seg)
                self.history.add_execution(
                    processor_name=self.cpu_names[idx],
                    metrics=cpu.metrics,
                    config=self.cpu_configs[idx]
                )
            except Exception as e:
                print(f"Error al ejecutar {self.cpu_names[idx]}: {e}")
        print("\n=== Comparación completada ===")
