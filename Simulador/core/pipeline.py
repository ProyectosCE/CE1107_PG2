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

"""
Class: Pipeline
Clase que simula el pipeline de un procesador, gestionando el avance de instrucciones por las etapas clásicas.

Attributes:
- IF_ID: dict - registro entre las etapas IF e ID, contiene al menos la instrucción y el PC.
- ID_EX: dict - registro entre las etapas ID y EX.
- EX_MEM: dict - registro entre las etapas EX y MEM.
- MEM_WB: dict - registro entre las etapas MEM y WB.
- completed: bool - indica si el pipeline está vacío (todas las etapas con NOP).
- cycles: int - número de ciclos ejecutados.

Constructor:
- __init__: Inicializa los registros del pipeline y los contadores.

Methods:
- init_pipeline: Inicializa los registros del pipeline con instrucciones NOP.
- step: Simula un ciclo del pipeline, avanzando las instrucciones una etapa.
- dump_pipeline: Devuelve el estado actual de todas las etapas.
- _create_nop_instruction: Crea una instrucción NOP interna.
- is_done: Indica si el pipeline está vacío.
- get_cycle: Devuelve el número de ciclos ejecutados.
- insert_stall: Inserta una burbuja (NOP) en la etapa ID/EX para resolver hazards.
- flush: Limpia las etapas IF/ID e ID/EX para anular instrucciones mal predichas.

Example:
    pipe = Pipeline()
    pipe.init_pipeline()
    while not pipe.is_done():
        pipe.step(Instruction("add x1, x2, x3", 0), 0)
"""

class Pipeline:
    def __init__(self):
        """
        Function: __init__
        Inicializa los registros del pipeline y los contadores de estado.
        """
        # Representan los registros entre etapas
        # cada uno es un diccionario con al menos una clave 'instr' que contiene la instrucción
        self._IF_ID = None
        self._ID_EX = None
        self._EX_MEM = None
        self._MEM_WB = None
        self.completed = False
        self.cycles = 0

    # --- Propiedades para acceso externo seguro ---
    @property
    def IF_ID(self):
        return self._IF_ID

    @IF_ID.setter
    def IF_ID(self, value):
        self._IF_ID = value

    @property
    def ID_EX(self):
        return self._ID_EX

    @ID_EX.setter
    def ID_EX(self, value):
        self._ID_EX = value

    @property
    def EX_MEM(self):
        return self._EX_MEM

    @EX_MEM.setter
    def EX_MEM(self, value):
        self._EX_MEM = value

    @property
    def MEM_WB(self):
        return self._MEM_WB

    @MEM_WB.setter
    def MEM_WB(self, value):
        self._MEM_WB = value

    def init_pipeline(self):
        """
        Function: init_pipeline
        Inicializa los registros del pipeline con instrucciones NOP y reinicia los contadores.
        Example:
            pipe.init_pipeline()
        """
        nop = self._create_nop_instruction()
        self.IF_ID = {"instr": nop, "pc": 0}
        self.ID_EX = {"instr": nop}
        self.EX_MEM = {"instr": nop}
        self.MEM_WB = {"instr": nop}
        self.completed = False
        self.cycles = 0

    def step(self, fetched_instr: Instruction, pc: int):
        """
        Function: step
        Simula un paso del pipeline, avanzando las instrucciones una etapa hacia adelante.
        Params:
        - fetched_instr: Instruction - instrucción obtenida en la etapa IF.
        - pc: int - dirección de la instrucción obtenida.
        Example:
            pipe.step(instr, 0)
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

    def dump_pipeline(self):
        """
        Function: dump_pipeline
        Retorna el estado actual de todas las etapas del pipeline para depuración o visualización.
        Returns:
        - dict: estado de los registros inter-etapas.
        Example:
            estado = pipe.dump_pipeline()
        """
        return {
            "IF_ID": self.IF_ID,
            "ID_EX": self.ID_EX,
            "EX_MEM": self.EX_MEM,
            "MEM_WB": self.MEM_WB
        }

    def _create_nop_instruction(self) -> Instruction:
        """
        Function: _create_nop_instruction
        Crea una instrucción NOP simulada (interna).
        Returns:
        - Instruction: instrucción NOP.
        Example:
            nop = self._create_nop_instruction()
        """
        return Instruction("nop", address=0)

    def is_done(self) -> bool:
        """
        Function: is_done
        Indica si el pipeline está vacío (todas las etapas contienen NOP).
        Returns:
        - bool: True si el pipeline está vacío, False en caso contrario.
        Example:
            if pipe.is_done():
                ...
        """
        return self.completed

    def get_cycle(self) -> int:
        """
        Function: get_cycle
        Devuelve el número de ciclos ejecutados por el pipeline.
        Returns:
        - int: número de ciclos.
        Example:
            ciclos = pipe.get_cycle()
        """
        return self.cycles

    def insert_stall(self):
        """
        Function: insert_stall
        Inserta una burbuja (NOP) en la etapa ID/EX sin avanzar la instrucción en IF/ID.
        Usado típicamente para resolver un load-use hazard.
        Example:
            pipe.insert_stall()
        """
        nop = self._create_nop_instruction()

        self.cycles += 1

        self.MEM_WB = self.EX_MEM
        self.EX_MEM = self.ID_EX
        self.ID_EX = {
            "instr": nop,
            "pc": self.IF_ID["pc"],
            "rd": None,
            "rs1": None,
            "rs2": None,
            "rs1_val": None,
            "rs2_val": None,
            "imm": None
        }
    # IF_ID no se modifica → mismo fetch, se repite la instrucción

    def flush(self):
        """
        Function: flush
        Limpia las etapas IF/ID e ID/EX para anular instrucciones mal predichas (por ejemplo, en saltos).
        Example:
            pipe.flush()
        """
        nop = self._create_nop_instruction()

        self.IF_ID = {"instr": nop, "pc": 0}
        self.ID_EX = {
            "instr": nop,
            "pc": 0,
            "rd": None,
            "rs1": None,
            "rs2": None,
            "rs1_val": None,
            "rs2_val": None,
            "imm": None
        }
