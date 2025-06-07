from core.pipeline import Pipeline
from core.stage_if import InstructionFetch
from core.stage_id import InstructionDecode
from core.stage_ex import ExecuteStage
from components.register_file import RegisterFile
from components.memory import Memory
from core.instruction import Instruction


class Processor:
    def __init__(self):
        self.instr_mem = Memory(size_in_words=64)
        self.pipeline = Pipeline()
        self.if_stage = InstructionFetch(self.instr_mem)
        self.registers = RegisterFile()
        self.id_stage = InstructionDecode(self.registers)
        self.ex_stage = ExecuteStage()

    def load_program(self, instr_list: list[str]):
        for i, line in enumerate(instr_list):
            pc = i * 4
            instr = Instruction(line, pc)
            self.instr_mem.store_word(pc, instr)

    def preload_registers(self, values: dict):
        for reg, val in values.items():
            self.registers.write(reg, val)

    def run(self):
        print("Iniciando simulación del procesador (IF → ID → EX)\n")
        self.pipeline.init_pipeline()

        while not self.pipeline.is_done():
            # 1. Instruction Fetch
            fetched = self.if_stage.fetch()
            instr = fetched["instr"]
            pc = fetched["pc"]
            self.pipeline.step(instr, pc)

            # 2. Instruction Decode
            if_id = self.pipeline.IF_ID
            id_ex = self.id_stage.decode(if_id)

            # 3. Execute Stage
            ex_result = self.ex_stage.execute(id_ex)

            # 4. Imprimir ciclo
            print(f"\n[Ciclo {self.pipeline.get_cycle()}]")
            print(f"IF_ID: {if_id['instr'].opcode} @ PC={if_id['pc']}")
            if id_ex["instr"].opcode != "nop":
                print(f"ID_EX: {id_ex['instr'].opcode}, rs1={id_ex['rs1']}={id_ex['rs1_val']}, "
                      f"rs2={id_ex['rs2']}={id_ex['rs2_val']}, imm={id_ex['imm']}, rd={id_ex['rd']}")
            else:
                print("ID_EX: nop")

            if ex_result["instr"].opcode != "nop":
                print(f"EX_MEM: {ex_result['instr'].opcode}, ALU={ex_result['alu_result']}, "
                      f"branch_taken={ex_result['branch_taken']}, target={ex_result['target_address']}")
            else:
                print("EX_MEM: nop")

        print("\n Programa finalizado. Pipeline vacío.")
