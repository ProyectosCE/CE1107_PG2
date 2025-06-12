from core.instruction import Instruction


class Pipeline:
    def __init__(self):
        # Representan los registros entre etapas
        # cada uno es un diccionario con al menos una clave 'instr' que contiene la instrucción
        self.IF_ID = None
        self.ID_EX = None
        self.EX_MEM = None
        self.MEM_WB = None
        self.completed = False
        self.cycles = 0

    def init_pipeline(self):
        """Inicializa los registros del pipeline con NOPs."""
        nop = self._create_nop_instruction()
        self.IF_ID = {"instr": nop, "pc": 0}
        self.ID_EX = {"instr": nop}
        self.EX_MEM = {"instr": nop}
        self.MEM_WB = {"instr": nop}
        self.completed = False
        self.cycles = 0

    #Simula un paso del pipeline cada instrucción avanza una etapa
    def step(self, fetched_instr: Instruction, pc: int):
        """
        Simula un paso del pipeline:
        Avanza las instrucciones una etapa hacia adelante.
        'fetched_instr' simula la salida del Instruction Fetch (IF).
        """
        self.cycles += 1

        # Avanzar pipeline (WB ya sale del sistema)
        self.MEM_WB = self.EX_MEM
        self.EX_MEM = self.ID_EX
        self.ID_EX = self.IF_ID
        self.IF_ID = {"instr": fetched_instr, "pc": pc}

        # Verificar si se ha completado (todas son NOP)
        if all(stage["instr"].opcode == "nop" for stage in
               [self.IF_ID, self.ID_EX, self.EX_MEM, self.MEM_WB]):
            self.completed = True

    # Devuelve estado actual del pipeline para GUI
    def dump_pipeline(self):
        """Retorna el estado actual de todas las etapas para depuración."""
        return {
            "IF_ID": self.IF_ID,
            "ID_EX": self.ID_EX,
            "EX_MEM": self.EX_MEM,
            "MEM_WB": self.MEM_WB
        }

    def _create_nop_instruction(self) -> Instruction:
        """Crea una instrucción NOP simulada (interna)."""
        return Instruction("nop", address=0)

    def is_done(self) -> bool:
        """Indica si el pipeline está vacío."""
        return self.completed

    def get_cycle(self) -> int:
        """Devuelve el número de ciclos ejecutados."""
        return self.cycles#
