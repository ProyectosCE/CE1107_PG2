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
        self.instr_mem = Memory(size_in_words=64)
        self.data_mem = Memory(size_in_words=64)
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
        """
        Ejecuta el procesador en diferentes modos:
        - modo="full": ejecución inmediata (por defecto)
        - modo="step": paso a paso, espera input del usuario
        - modo="delay": espera delay_seg segundos entre ciclos
        """
        self.pipeline.init_pipeline()

        while not self.pipeline.is_done():
            self.metrics.tick()  

            hazard_info = self.hazard_unit.detect_hazard(
                self.pipeline.IF_ID,
                self.pipeline.ID_EX,
                self.pipeline.EX_MEM,
                self.pipeline.MEM_WB
            )

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

            if ex_mem["instr"].opcode in {"beq", "bne", "jal"}:
                predicted = id_ex.get("predicted_taken", False)
                actual = ex_mem.get("branch_taken", False)
                self.metrics.track_branch(predicted, actual)

            if ex_mem.get("flush_required", False):
                self.pipeline.flush()

            mem_wb = self.mem_stage.access(ex_mem)
            self.wb_stage.write_back(mem_wb)

            self.metrics.track_writeback(mem_wb["instr"])

            # Prints por etapa
            print(f"\n[Ciclo {self.pipeline.get_cycle()}]")
            print(f"IF_ID: {if_id['instr'].opcode} @ PC={if_id['pc']}")

            if id_ex["instr"].opcode != "nop":
                print(f"ID_EX: {id_ex['instr'].opcode}, rs1={id_ex['rs1']}={id_ex['rs1_val']}, "
                      f"rs2={id_ex['rs2']}={id_ex['rs2_val']}, imm={id_ex['imm']}, rd={id_ex['rd']}")
            else:
                print("ID_EX: nop")

            if ex_mem["instr"].opcode != "nop":
                print(f"EX_MEM: {ex_mem['instr'].opcode}, ALU={ex_mem['alu_result']}, "
                      f"branch_taken={ex_mem['branch_taken']}, target={ex_mem['target_address']}")
            else:
                print("EX_MEM: nop")

            if mem_wb["instr"].opcode == "lw":
                print(f"MEM_WB: lw → {mem_wb['rd']} = {mem_wb['mem_data']}")
            elif mem_wb["instr"].opcode == "sw":
                print(f"MEM_WB: sw → mem[{ex_mem['alu_result']}] = {ex_mem['rs2_val']}")
            elif mem_wb["instr"].opcode != "nop":
                print(f"MEM_WB: {mem_wb['instr'].opcode}, ALU result = {mem_wb['alu_result']}")
            else:
                print("MEM_WB: nop")

            # --- Modo de ejecución ---
            if modo == "step":
                input("Presione Enter para continuar al siguiente ciclo...")
            elif modo == "delay":
                time.sleep(delay_seg)
            # modo "full" no hace nada extra

        print("\nPrograma finalizado (Procesador Completo). Pipeline vacío.")

        self.metrics.display()

    def get_metrics(self):
        return self.metrics
