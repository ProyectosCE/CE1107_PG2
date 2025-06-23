from core.pipeline import Pipeline
from core.stage_if import InstructionFetch
from core.stage_id_basic import InstructionDecodeBasic
from core.stage_ex_basic import ExecuteStageBasic
from core.stage_mem import MemoryAccessStage
from core.stage_wb import WriteBackStage
from components.register_file import RegisterFile
from components.memory import Memory
from core.instruction import Instruction
from InOut.metrics import Metrics             
import time

class ProcessorBasic:
    """Procesador sin unidad de hazards ni predicción de saltos."""
    def __init__(self):
        self.instr_mem = Memory(size_in_words=1024)
        self.data_mem  = Memory(size_in_words=1024)
        self.pipeline  = Pipeline()

        self.if_stage  = InstructionFetch(self.instr_mem, latency=None)
        self.registers = RegisterFile()
        self.id_stage  = InstructionDecodeBasic(self.registers, latency=None)
        self.ex_stage  = ExecuteStageBasic(latency=None)
        self.mem_stage = MemoryAccessStage(self.data_mem, latency=None)
        self.wb_stage  = WriteBackStage(self.registers, latency=None)

        self.metrics   = Metrics(name="Processor Básico")   

    def load_program(self, instr_list: list[str]):
        for i, line in enumerate(instr_list):
            pc = i * 4
            self.instr_mem.store_word(pc, Instruction(line, pc))

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

        last_ex_mem = None

        while not self.pipeline.is_done():
            self.metrics.tick()                      

            # --- CONTROL DE SALTOS (básico, sin predicción) ---
            if last_ex_mem and last_ex_mem["instr"].opcode in {"beq", "bne", "jal"}:
                if last_ex_mem.get("branch_taken", False):
                    target = last_ex_mem.get("target_address")
                    if target is not None:
                        self.if_stage.jump(target)

            fetched = self.if_stage.fetch()
            self.pipeline.step(fetched["instr"], fetched["pc"])

            if_id  = self.pipeline.IF_ID
            id_ex  = self.id_stage.decode(if_id)
            ex_mem = self.ex_stage.execute(id_ex)
            last_ex_mem = ex_mem  # Guardar para el siguiente ciclo

            mem_wb = self.mem_stage.access(ex_mem)
            self.wb_stage.write_back(mem_wb)

            self.metrics.track_writeback(mem_wb["instr"])

            

            # --- Modo de ejecución ---
            if modo == "step":
                input("Presione Enter para continuar al siguiente ciclo...")
            elif modo == "delay":
                time.sleep(delay_seg)
            # modo "full" no hace nada extra

        print("\nPrograma finalizado (ProcessorBasic). Pipeline vacío.")
        self.metrics.display()                         

    def get_metrics(self):
        return self.metrics
