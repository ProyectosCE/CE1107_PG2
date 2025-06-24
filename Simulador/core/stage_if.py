"""
================================== LICENCIA ==============================
MIT License
Copyright (c) 2025 José Bernardo Barquero Bonilla,
Jose Eduardo Campos Salazar,
Jimmy Feng Feng,
Alexander Montero Vargas
Consulta el archivo LICENSE para más detalles.
==========================================================================
"""

from core.instruction import Instruction
from components.memory import Memory
import time
from config import LATENCY_IF

"""
Class: InstructionFetch
Clase que representa la etapa de búsqueda de instrucciones (IF) del pipeline, encargada de obtener la instrucción desde memoria y avanzar el PC.

Attributes:
- instr_mem: Memory - referencia a la memoria de instrucciones.
- pc: int - contador de programa (dirección de la siguiente instrucción).
- halted: bool - indica si se ha alcanzado el final del programa.

Constructor:
- __init__: Inicializa la etapa IF con la memoria de instrucciones.

Methods:
- fetch: Obtiene la instrucción actual y avanza el PC.
- jump: Modifica el PC para saltos de control.
- _create_nop: Crea una instrucción NOP.
- reset: Restablece el PC y el estado de halted.
- get_pc: Devuelve el valor actual del PC.

Example:
    if_stage = InstructionFetch(mem)
    fetch_result = if_stage.fetch()
"""

class InstructionFetch:
    def __init__(self, instruction_memory: Memory, latency: float = None):
        """
        Function: __init__
        Inicializa la etapa IF con acceso a la memoria de instrucciones.
        Params:
        - instruction_memory: Memory - memoria de instrucciones.
        Example:
            if_stage = InstructionFetch(mem)
        """
        self.instr_mem = instruction_memory
        self.pc = 0  # PC inicia en 0
        self.halted = False
        self.latency = latency if latency is not None else LATENCY_IF

    def fetch(self) -> dict:
        """
        Function: fetch
        Obtiene la instrucción actual y avanza el PC para el siguiente ciclo.
        Si no hay más instrucciones, devuelve una instrucción NOP y marca el estado como halted.
        Returns:
        - dict: contiene 'instr' (Instruction) y 'pc' (int).
        Example:
            resultado = if_stage.fetch()
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
        time.sleep(self.latency)

        return {"instr": instr, "pc": current_pc}

    def jump(self, new_address: int):
        """
        Function: jump
        Modifica el PC para saltos de control (jal, beq, etc).
        Params:
        - new_address: int - nueva dirección para el PC.
        Example:
            if_stage.jump(16)
        """
        self.pc = new_address

    def _create_nop(self) -> Instruction:
        """
        Function: _create_nop
        Crea una instrucción NOP en la dirección actual del PC.
        Returns:
        - Instruction: instrucción NOP.
        Example:
            nop = self._create_nop()
        """
        return Instruction("nop", self.pc)

    def reset(self):
        """
        Function: reset
        Restablece el PC a 0 y el estado de halted para reiniciar la simulación.
        Example:
            if_stage.reset()
        """
        self.pc = 0
        self.halted = False

    def get_pc(self) -> int:
        """
        Function: get_pc
        Devuelve el valor actual del PC.
        Returns:
        - int: valor del PC.
        Example:
            pc_actual = if_stage.get_pc()
        """
        return self.pc
