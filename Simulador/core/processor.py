from core.pipeline import Pipeline
from core.stage_if import InstructionFetch
from core.stage_id import InstructionDecode
from core.stage_ex import ExecuteStage
from core.stage_mem import MemoryAccessStage
from core.stage_wb import WriteBackStage
from components.register_file import RegisterFile
from components.memory import Memory
from components.hazard_unit import HazardUnit
from components.branch_predictor import BranchPredictor
from components.control_unit import ControlUnit  
from core.instruction import Instruction
from InOut.metrics import Metrics  
import time

class Processor:
    def __init__(self):
        self.instr_mem = Memory(size_in_words=1024)
        self.data_mem = Memory(size_in_words=1024)
        self.pipeline = Pipeline()

        self.if_stage = InstructionFetch(self.instr_mem, latency=None)
        self.registers = RegisterFile()
        self.hazard_unit = HazardUnit()
        self.branch_predictor = BranchPredictor()
        self.control_unit = ControlUnit()

        self.id_stage = InstructionDecode(self.registers, self.branch_predictor, self.control_unit, latency=None)
        self.ex_stage = ExecuteStage(self.branch_predictor, latency=None)
        self.mem_stage = MemoryAccessStage(self.data_mem, latency=None)
        self.wb_stage = WriteBackStage(self.registers, latency=None)

        self.metrics = Metrics(name="Procesador Completo")  

    def load_program(self, instr_list: list[str]):
        for i, line in enumerate(instr_list):
            pc = i * 4
            instr = Instruction(line, pc)
            self.instr_mem.store_word(pc, instr)

    def preload_registers(self, values: dict):
        for reg, val in values.items():
            self.registers.write(reg, val)

    def preload_data_memory(self, values: dict):
        for addr, val in values.items():
            self.data_mem.store_word(addr, val)

    def run(self, modo="full", delay_seg=1.0):
        self.metrics.start_timer()
        self.pipeline.init_pipeline()

        while not self.pipeline.is_done():
            self.metrics.tick()  

            hazard_info = self.hazard_unit.detect_hazard(
                self.pipeline.IF_ID,
                self.pipeline.ID_EX,
                self.pipeline.EX_MEM,
                self.pipeline.MEM_WB
            )

            # --- CONTROL DE SALTOS Y FLUSH ---
            # 1. Si la instrucción en EX_MEM es branch/jal y requiere flush, actualiza PC al destino real
            ex_mem = getattr(self, "last_ex_mem", None)
            if ex_mem and ex_mem.get("flush_required", False):
                # Se resolvió un branch tomado o mala predicción: saltar al destino real
                target = ex_mem.get("target_address")
                if target is not None:
                    self.if_stage.jump(target)
                self.pipeline.flush()
            # 2. Si la instrucción en ID_EX es branch/jal y la predicción fue tomada, saltar al destino predicho
            else:
                id_ex_prev = getattr(self, "last_id_ex", None)
                if id_ex_prev and id_ex_prev["instr"].opcode in {"beq", "bne", "jal"}:
                    if id_ex_prev.get("predicted_taken", False):
                        predicted_target = id_ex_prev.get("predicted_target")
                        if predicted_target is not None:
                            self.if_stage.jump(predicted_target)

            if hazard_info["stall"]:
                print("Hazard detectado → STALL aplicado (load-use)")
                self.pipeline.insert_stall()
            else:
                fetched = self.if_stage.fetch()
                instr = fetched["instr"]
                pc = fetched["pc"]
                self.pipeline.step(instr, pc)

            if_id = self.pipeline.IF_ID
            id_ex = self.id_stage.decode(if_id)
            ex_mem = self.ex_stage.execute(id_ex)
            self.last_id_ex = id_ex  # Guardar para el siguiente ciclo
            self.last_ex_mem = ex_mem  # Guardar para el siguiente ciclo

            if ex_mem["instr"].opcode in {"beq", "bne", "jal"}:
                predicted = id_ex.get("predicted_taken", False)
                actual = ex_mem.get("branch_taken", False)
                self.metrics.track_branch(predicted, actual)

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
        print("\nPrograma finalizado (Procesador Completo). Pipeline vacío.")

        self.metrics.display()

    def get_metrics(self):
        return self.metrics
        self.metrics.display()

        self.metrics.report()

    def run_one_cycle(self):
        """Avanza un ciclo del pipeline. Retorna True si terminó, False si no."""
        if not hasattr(self, "_step_pipeline_initialized") or not self._step_pipeline_initialized:
            self.metrics.start_timer()
            self.pipeline.init_pipeline()
            self._step_pipeline_initialized = True
            self.last_id_ex = None
            self.last_ex_mem = None

        if self.pipeline.is_done():
            self.metrics.stop_timer()
            return True

        self.metrics.tick()

        hazard_info = self.hazard_unit.detect_hazard(
            self.pipeline.IF_ID,
            self.pipeline.ID_EX,
            self.pipeline.EX_MEM,
            self.pipeline.MEM_WB
        )

        # --- CONTROL DE SALTOS Y FLUSH ---
        ex_mem = getattr(self, "last_ex_mem", None)
        if ex_mem and ex_mem.get("flush_required", False):
            target = ex_mem.get("target_address")
            if target is not None:
                self.if_stage.jump(target)
            self.pipeline.flush()
        else:
            id_ex_prev = getattr(self, "last_id_ex", None)
            if id_ex_prev and id_ex_prev["instr"].opcode in {"beq", "bne", "jal"}:
                if id_ex_prev.get("predicted_taken", False):
                    predicted_target = id_ex_prev.get("predicted_target")
                    if predicted_target is not None:
                        self.if_stage.jump(predicted_target)

        if hazard_info["stall"]:
            # print("Hazard detectado → STALL aplicado (load-use)")
            self.pipeline.insert_stall()
        else:
            fetched = self.if_stage.fetch()
            instr = fetched["instr"]
            pc = fetched["pc"]
            self.pipeline.step(instr, pc)

        if_id = self.pipeline.IF_ID
        id_ex = self.id_stage.decode(if_id)
        ex_mem = self.ex_stage.execute(id_ex)
        self.last_id_ex = id_ex  # Guardar para el siguiente ciclo
        self.last_ex_mem = ex_mem  # Guardar para el siguiente ciclo

        if ex_mem["instr"].opcode in {"beq", "bne", "jal"}:
            predicted = id_ex.get("predicted_taken", False)
            actual = ex_mem.get("branch_taken", False)
            self.metrics.track_branch(predicted, actual)

        mem_wb = self.mem_stage.access(ex_mem)
        self.wb_stage.write_back(mem_wb)

        self.metrics.track_writeback(mem_wb["instr"])

        if self.pipeline.is_done():
            self.metrics.stop_timer()
            return True
        return False

