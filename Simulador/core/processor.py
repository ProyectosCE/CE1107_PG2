from core.pipeline import Pipeline
from core.stage_if import InstructionFetch
from core.stage_id import InstructionDecode
from components.register_file import RegisterFile
from components.memory import Memory
from core.instruction import Instruction

class Processor:
    def __init__(self):
        self.instr_mem = Memory(size_in_words=64)  # Memoria para 256 bytes
        self.pipeline = Pipeline()
        self.if_stage = InstructionFetch(self.instr_mem)
        self.registers = RegisterFile()
        self.id_stage = InstructionDecode(self.registers)

    def load_program(self, instr_list: list[str]):
        """
        Carga un programa como lista de instrucciones tipo string.
        """
        for i, line in enumerate(instr_list):
            pc = i * 4
            instr = Instruction(line, pc)
            self.instr_mem.store_word(pc, instr)

    def preload_registers(self, values: dict):
        """
        Carga valores iniciales en el banco de registros.
        Ejemplo: { "x2": 10, "x3": 20 }
        """
        for reg, val in values.items():
            self.registers.write(reg, val)

    def run(self):
        """
        Ejecuta el programa paso a paso y muestra estado de IF y ID.
        """
        print("Iniciando simulación del procesador (IF + ID)...\n")
        self.pipeline.init_pipeline()

        while not self.pipeline.is_done():
            # Obtener instrucción desde la etapa IF
            fetched = self.if_stage.fetch()
            instr = fetched["instr"]
            pc = fetched["pc"]

            # Avanzar pipeline (instrucción nueva entra al frente)
            self.pipeline.step(instr, pc)

            # Decodificar lo que hay en IF/ID
            if_id = self.pipeline.IF_ID
            id_ex = self.id_stage.decode(if_id)

            # Imprimir resultados del ciclo
            print(f"\n[Ciclo {self.pipeline.get_cycle()}]")
            print(f"IF_ID: {if_id['instr'].opcode} @ PC={if_id['pc']}")
            if id_ex["instr"].opcode != "nop":
                print(f"ID_EX: {id_ex['instr'].opcode}, rs1={id_ex['rs1']}={id_ex['rs1_val']}, "
                      f"rs2={id_ex['rs2']}={id_ex['rs2_val']}, rd={id_ex['rd']}")
            else:
                print("ID_EX: nop")

        print("\n Programa finalizado. Pipeline vacío.")
