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

class ProcessorNoHazards:
    """
    Simula un procesador con forwarding habilitado (sin unidad de riesgos explícita),
    lo que permite evitar stalls en muchos casos comunes.
    """
    def __init__(self):
        self.instr_mem = Memory(size_in_words=1024)
        self.data_mem = Memory(size_in_words=1024)
        self.pipeline = Pipeline()

        self.if_stage = InstructionFetch(self.instr_mem, latency=None)
        self.registers = RegisterFile()
        self.id_stage = InstructionDecodeBasic(self.registers, latency=None)  # Sin unidad de control/predictor
        self.ex_stage = ExecuteStageBasic(latency=None)                     # Sin predicción
        self.mem_stage = MemoryAccessStage(self.data_mem, latency=None)
        self.wb_stage = WriteBackStage(self.registers, latency=None)

        self.metrics = Metrics(name="Processor Sin Unidad de Riesgos")

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

        last_ex_mem = None

        while not self.pipeline.is_done():
            self.metrics.tick()

            # --- CONTROL DE SALTOS (sin predicción) ---
            if last_ex_mem and last_ex_mem["instr"].opcode in {"beq", "bne", "jal"}:
                if last_ex_mem.get("branch_taken", False):
                    target = last_ex_mem.get("target_address")
                    if target is not None:
                        self.if_stage.jump(target)

            # 1. IF
            fetched = self.if_stage.fetch()
            instr = fetched["instr"]
            pc = fetched["pc"]
            self.pipeline.step(instr, pc)

            # 2. ID
            if_id = self.pipeline.IF_ID
            id_ex = self.id_stage.decode(if_id)

            # 3. EX
            ex_mem = self.ex_stage.execute(id_ex)
            # --- Agrega control_signals para instrucciones que escriben en registros ---
            opcode = ex_mem["instr"].opcode
            regwrite_opcodes = {
                "add", "sub", "and", "or", "xor", "slt", "sll", "srl", "sra",
                "addi", "andi", "ori", "slti", "slli", "srli", "srai",
                "lui", "auipc", "jal", "jalr", "lw"
            }
            ex_mem["control_signals"] = {}
            if opcode in regwrite_opcodes:
                ex_mem["control_signals"]["RegWrite"] = True
            if opcode == "lw":
                ex_mem["control_signals"]["MemToReg"] = True
            if opcode == "lw":
                ex_mem["control_signals"]["MemRead"] = True
            if opcode == "sw":
                ex_mem["control_signals"]["MemWrite"] = True

            last_ex_mem = ex_mem  # Guardar para el siguiente ciclo

            # 4. MEM
            mem_wb = self.mem_stage.access(ex_mem)
            # --- Propaga control_signals a mem_wb ---
            mem_wb["control_signals"] = ex_mem.get("control_signals", {})

            # 5. WB
            self.wb_stage.write_back(mem_wb)
            self.metrics.track_writeback(mem_wb["instr"])

            # --- Modo de ejecución ---
            if modo == "step":
                input("Presione Enter para continuar al siguiente ciclo...")
            elif modo == "delay":
                time.sleep(delay_seg)
            # modo "full" no hace nada extra

        self.metrics.stop_timer()
        print("\n Programa finalizado (ProcessorNoHazards). Pipeline vacío.")
        self.metrics.display()
            # modo "full" no hace nada extra

        print("\n Programa finalizado (ProcessorNoHazards). Pipeline vacío.")
        self.metrics.display()
    
    def run_one_cycle(self):
        """Avanza un ciclo del pipeline. Retorna True si terminó, False si no."""
        if not hasattr(self, "_step_pipeline_initialized") or not self._step_pipeline_initialized:
            self.metrics.start_timer()
            self._step_start_time = time.perf_counter()
            self.pipeline.init_pipeline()
            self._step_pipeline_initialized = True
            self._last_ex_mem = None

        if self.pipeline.is_done():
            self.metrics.stop_timer()
            return True

        self.metrics.tick()

        # --- CONTROL DE SALTOS (sin predicción) ---
        if hasattr(self, "_last_ex_mem") and self._last_ex_mem and self._last_ex_mem["instr"].opcode in {"beq", "bne", "jal"}:
            if self._last_ex_mem.get("branch_taken", False):
                target = self._last_ex_mem.get("target_address")
                if target is not None:
                    self.if_stage.jump(target)

        # 1. IF
        fetched = self.if_stage.fetch()
        instr = fetched["instr"]
        pc = fetched["pc"]
        self.pipeline.step(instr, pc)

        # 2. ID
        if_id = self.pipeline.IF_ID
        id_ex = self.id_stage.decode(if_id)

        # 3. EX
        ex_mem = self.ex_stage.execute(id_ex)
        # --- Agrega control_signals para instrucciones que escriben en registros ---
        opcode = ex_mem["instr"].opcode
        regwrite_opcodes = {
            "add", "sub", "and", "or", "xor", "slt", "sll", "srl", "sra",
            "addi", "andi", "ori", "slti", "slli", "srli", "srai",
            "lui", "auipc", "jal", "jalr", "lw"
        }
        ex_mem["control_signals"] = {}
        if opcode in regwrite_opcodes:
            ex_mem["control_signals"]["RegWrite"] = True
        if opcode == "lw":
            ex_mem["control_signals"]["MemToReg"] = True
        if opcode == "lw":
            ex_mem["control_signals"]["MemRead"] = True
        if opcode == "sw":
            ex_mem["control_signals"]["MemWrite"] = True

        self._last_ex_mem = ex_mem  # Guardar para el siguiente ciclo

        # 4. MEM
        mem_wb = self.mem_stage.access(ex_mem)
        # --- Propaga control_signals a mem_wb ---
        mem_wb["control_signals"] = ex_mem.get("control_signals", {})

        # 5. WB
        self.wb_stage.write_back(mem_wb)
        self.metrics.track_writeback(mem_wb["instr"])

        # Actualiza el tiempo de ejecución en cada ciclo
        if hasattr(self, "_step_start_time"):
            self.metrics.elapsed_time = time.perf_counter() - self._step_start_time

        if self.pipeline.is_done():
            self.metrics.stop_timer()
            return True
        return False
