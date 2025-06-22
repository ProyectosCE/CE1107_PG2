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

class ProcessorNoHazards:
    """
    Simula un procesador con forwarding habilitado (sin unidad de riesgos explícita),
    lo que permite evitar stalls en muchos casos comunes.
    """
    def __init__(self):
        self.instr_mem = Memory(size_in_words=64)
        self.data_mem = Memory(size_in_words=64)
        self.pipeline = Pipeline()

        self.if_stage = InstructionFetch(self.instr_mem)
        self.registers = RegisterFile()
        self.id_stage = InstructionDecodeBasic(self.registers)  # Sin unidad de control/predictor
        self.ex_stage = ExecuteStageBasic()                     # Sin predicción
        self.mem_stage = MemoryAccessStage(self.data_mem)
        self.wb_stage = WriteBackStage(self.registers)

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

    def run(self):
        self.pipeline.init_pipeline()

        while not self.pipeline.is_done():
            self.metrics.tick()

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

            # 4. MEM
            mem_wb = self.mem_stage.access(ex_mem)

            # 5. WB
            self.wb_stage.write_back(mem_wb)
            self.metrics.track_writeback(mem_wb["instr"])

            # Imprimir estado por etapa
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

        print("\n Programa finalizado (ProcessorNoHazards). Pipeline vacío.")
        self.metrics.display()
