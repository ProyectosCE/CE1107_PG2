from core.pipeline import Pipeline
from core.stage_if import InstructionFetch
from core.stage_id import InstructionDecode
from core.stage_mem import MemoryAccessStage
from core.stage_wb import WriteBackStage
from components.register_file import RegisterFile
from components.memory import Memory
from components.hazard_unit import HazardUnit
from components.control_unit import ControlUnit
from InOut.metrics import Metrics
from core.instruction import Instruction
import time

class NullBranchPredictor:
    def predict(self, pc):
        return {"taken": False}

    def update(self, pc, actual):
        pass

    def flush_required(self, predicted, actual):
        # siempre hay que hacer flush si el branch se toma (predicted=False, actual=True)
        return actual and not predicted

from core.stage_ex_basic import ExecuteStageBasic

class ExecuteStageNoPredictor(ExecuteStageBasic):
    """Extiende la versión básica para indicar flush cuando se detecta un salto tomado."""
    def execute(self, id_ex: dict) -> dict:
        res = super().execute(id_ex)
        # Si es branch / jal y se toma → flush requerido
        opcode = res["instr"].opcode
        if opcode in {"beq", "bne", "jal"} and res["branch_taken"]:
            res["flush_required"] = True
        return res

class ProcessorNoPredictor:
    """Procesador con unidad de riesgos (stalls), pero SIN predicción de saltos."""

    def __init__(self):
        self.instr_mem = Memory(size_in_words=1024)
        self.data_mem  = Memory(size_in_words=1024)
        self.pipeline  = Pipeline()

        # Etapas
        self.if_stage  = InstructionFetch(self.instr_mem, latency=None)
        self.registers = RegisterFile()
        self.hazard_unit = HazardUnit()          # detecta riesgos → stalls
        self.control_unit = ControlUnit()
        self.branch_predictor = NullBranchPredictor()

        from core.stage_ex_basic import ExecuteStageBasic  # base para ALU
        self.id_stage  = InstructionDecode(self.registers, self.branch_predictor, self.control_unit, latency=None)
        self.ex_stage  = ExecuteStageNoPredictor(latency=None)
        self.mem_stage = MemoryAccessStage(self.data_mem, latency=None)
        self.wb_stage  = WriteBackStage(self.registers, latency=None)

        self.metrics   = Metrics(name="Processor sin Predictor (con hazards)")

    def load_program(self, instr_list: list[str]):
        for i, line in enumerate(instr_list):
            pc = i * 4
            self.instr_mem.store_word(pc, Instruction(line, pc))

    def preload_registers(self, values: dict):
        for r, v in values.items():
            self.registers.write(r, v)

    def preload_data_memory(self, values: dict):
        for a, v in values.items():
            self.data_mem.store_word(a, v)

    def run(self, modo="full", delay_seg=1.0):
        self.metrics.start_timer()
        self.pipeline.init_pipeline()

        last_ex_mem = None

        while not self.pipeline.is_done():
            self.metrics.tick()

            hazard = self.hazard_unit.detect_hazard(
                self.pipeline.IF_ID,
                self.pipeline.ID_EX,
                self.pipeline.EX_MEM,
                self.pipeline.MEM_WB,
            )
            # --- CONTROL DE SALTOS Y FLUSH ---
            if last_ex_mem and last_ex_mem.get("flush_required", False):
                target = last_ex_mem.get("target_address")
                if target is not None:
                    self.if_stage.jump(target)
                self.pipeline.flush()
            # --- AVANCE NORMAL DEL PIPELINE ---
            if hazard["stall"]:
                print("STALL por riesgo tipo load-use")
                self.pipeline.insert_stall()
            else:
                fetched = self.if_stage.fetch()
                self.pipeline.step(fetched["instr"], fetched["pc"])

            if_id  = self.pipeline.IF_ID
            id_ex  = self.id_stage.decode(if_id)
            ex_mem = self.ex_stage.execute(id_ex)
            last_ex_mem = ex_mem  # Guardar para el siguiente ciclo

            # (flush ya se maneja arriba)

            mem_wb = self.mem_stage.access(ex_mem)
            self.wb_stage.write_back(mem_wb)
            self.metrics.track_writeback(mem_wb["instr"])

            

            # --- Modo de ejecución ---
            if modo == "step":
                input("Presione Enter para continuar al siguiente ciclo...")
            elif modo == "delay":
                time.sleep(delay_seg)
            # modo "full" no hace nada extra

        self.metrics.stop_timer()
        print("\n Programa finalizado (ProcessorNoPredictor). Pipeline vacío.")
        self.metrics.display()

    def get_metrics(self):
        return self.metrics
        self.metrics.display()

    def get_metrics(self):
        return self.metrics
