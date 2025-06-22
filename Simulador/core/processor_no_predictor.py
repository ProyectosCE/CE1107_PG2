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
        self.instr_mem = Memory(size_in_words=64)
        self.data_mem  = Memory(size_in_words=64)
        self.pipeline  = Pipeline()

        # Etapas
        self.if_stage  = InstructionFetch(self.instr_mem)
        self.registers = RegisterFile()
        self.hazard_unit = HazardUnit()          # detecta riesgos → stalls
        self.control_unit = ControlUnit()
        self.branch_predictor = NullBranchPredictor()

        from core.stage_ex_basic import ExecuteStageBasic  # base para ALU
        self.id_stage  = InstructionDecode(self.registers, self.branch_predictor, self.control_unit)
        self.ex_stage  = ExecuteStageNoPredictor()
        self.mem_stage = MemoryAccessStage(self.data_mem)
        self.wb_stage  = WriteBackStage(self.registers)

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

    def run(self):
        self.pipeline.init_pipeline()

        while not self.pipeline.is_done():
            self.metrics.tick()

            hazard = self.hazard_unit.detect_hazard(
                self.pipeline.IF_ID,
                self.pipeline.ID_EX,
                self.pipeline.EX_MEM,
                self.pipeline.MEM_WB,
            )
            if hazard["stall"]:
                print("STALL por riesgo tipo load-use")
                self.pipeline.insert_stall()
            else:
                fetched = self.if_stage.fetch()
                self.pipeline.step(fetched["instr"], fetched["pc"])

            if_id  = self.pipeline.IF_ID
            id_ex  = self.id_stage.decode(if_id)
            ex_mem = self.ex_stage.execute(id_ex)

            if ex_mem.get("flush_required", False):
                self.pipeline.flush()

            mem_wb = self.mem_stage.access(ex_mem)
            self.wb_stage.write_back(mem_wb)
            self.metrics.track_writeback(mem_wb["instr"])

        print("\n Programa finalizado (ProcessorNoPredictor). Pipeline vacío.")
        self.metrics.display()

    def get_metrics(self):
        return self.metrics
