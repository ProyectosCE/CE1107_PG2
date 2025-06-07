from core.instruction import Instruction
from components.memory import Memory


class InstructionFetch:
    def __init__(self, instruction_memory: Memory):
        """
        Crea la etapa IF con acceso a la memoria de instrucciones.
        """
        self.instr_mem = instruction_memory
        self.pc = 0  # PC inicia en 0
        self.halted = False

    def fetch(self) -> dict:
        """
        Devuelve un diccionario con:
        - La instrucción actual (Instruction)
        - El valor del PC actual
        Avanza el PC para el siguiente ciclo.

        Si no hay más instrucciones, devuelve una instrucción NOP y marca el estado como halted.
        """
        if self.halted:
            return {"instr": self._create_nop(), "pc": self.pc}

        try:
            instr_line = self.instr_mem.load_word(self.pc)
            if isinstance(instr_line, Instruction):
                instr = instr_line
            else:
                instr = Instruction(instr_line, self.pc)
        except Exception:
            instr = self._create_nop()
            self.halted = True

        current_pc = self.pc
        self.pc += 4  # Avanza a la siguiente instrucción

        return {"instr": instr, "pc": current_pc}

    def jump(self, new_address: int):
        """
        Permite modificar el PC en caso de saltos (jal, beq, etc.)
        """
        self.pc = new_address

    def _create_nop(self) -> Instruction:
        return Instruction("nop", self.pc)

    # Restablece el PC a 0 para reiniciar simulación
    def reset(self):
        self.pc = 0
        self.halted = False

    def get_pc(self) -> int:
        return self.pc
