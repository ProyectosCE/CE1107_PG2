from core.pipeline import Pipeline
from core.stage_if import InstructionFetch
from components.memory import Memory
from core.instruction import Instruction


class Processor:
    def __init__(self):
        self.instr_mem = Memory(size_in_words=64)  # Memoria para 256 bytes (64 instrucciones)
        self.pipeline = Pipeline()
        self.if_stage = InstructionFetch(self.instr_mem)

    def load_program(self, instr_list: list[str]):
        """
        Carga un programa como lista de strings tipo assembly (ya parseado o no).
        Se guarda en memoria como texto o como objetos Instruction.
        """
        for i, line in enumerate(instr_list):
            pc = i * 4
            instr = Instruction(line, pc)
            self.instr_mem.store_word(pc, instr)

    def run(self):
        """
        Simula la ejecución paso a paso de un programa.
        Muestra el estado del pipeline en cada ciclo.
        """
        print("Iniciando simulación del procesador...\n")
        self.pipeline.init_pipeline()

        while not self.pipeline.is_done():
            # Obtener la próxima instrucción desde IF
            fetched = self.if_stage.fetch()
            instr = fetched["instr"]
            pc = fetched["pc"]

            # Avanzar el pipeline
            self.pipeline.step(instr, pc)

            # Mostrar estado del pipeline
            print(f"\n[Ciclo {self.pipeline.get_cycle()}]")
            stages = self.pipeline.dump_pipeline()
            for stage, info in stages.items():
                op = info["instr"].opcode if info else "-"
                addr = info["pc"] if "pc" in info else "-"
                print(f"{stage}: {op} @ PC={addr}")

        print("\n Programa finalizado. Pipeline vacío.")
