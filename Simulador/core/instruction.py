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

from enum import Enum, auto

"""
Class: InstructionType
Enumeración que define los tipos de instrucciones soportados por el simulador.

Attributes:
(No aplica, es una enumeración)

Constructor:
(No aplica)

Methods:
(No aplica)

Example:
    tipo = InstructionType.R_TYPE
"""

class InstructionType(Enum):
    R_TYPE = auto()
    I_TYPE = auto()
    S_TYPE = auto()
    B_TYPE = auto()
    J_TYPE = auto()
    INVALID = auto()

"""
Class: Instruction
Clase que representa una instrucción individual en el simulador, permitiendo su decodificación y análisis.

Attributes:
- raw_text: str - texto original de la instrucción.
- address: int - dirección de memoria (PC) donde se encuentra la instrucción.
- opcode: str o None - operación principal de la instrucción.
- operands: list - lista de operandos (registros o valores inmediatos).
- type: InstructionType - tipo de instrucción según el opcode.
- rd: str o None - registro destino (si aplica).
- rs1: str o None - primer registro fuente (si aplica).
- rs2: str o None - segundo registro fuente (si aplica).
- imm: int o None - valor inmediato (si aplica).

Constructor:
- __init__: Recibe el texto crudo de la instrucción y su dirección, inicializa y decodifica los campos.

Methods:
- _parse_instruction: Decodifica la instrucción y llena los campos según el opcode.
- __str__: Devuelve una representación textual de la instrucción con su dirección.
- is_valid: Indica si la instrucción es válida o no.

Example:
    instr = Instruction("add x1, x2, x3", 0)
    print(instr.rd)  # Imprime: x1
    print(instr)     # Imprime la instrucción con dirección
"""

class Instruction:
    def __init__(self, raw_text: str, address: int):
        """
        Function: __init__
        Inicializa una instrucción, decodificando sus campos a partir del texto y la dirección.
        Params:
        - raw_text: str - texto original de la instrucción.
        - address: int - dirección de memoria (PC) de la instrucción.
        Example:
            instr = Instruction("addi x1, x2, 10", 4)
        """
        self.raw_text = raw_text.strip() # Línea original
        self.address = address  # Dirección en memoria (PC)
        self.opcode = None
        self.operands = []  # Lista de registros o valores
        self.type = InstructionType.INVALID # Tipo de instrucción (determinado por el opcode)

        # Campos decodificados
        self.rd = None
        self.rs1 = None
        self.rs2 = None
        self.imm = None

        self._parse_instruction()

    def _parse_instruction(self):
        """
        Function: _parse_instruction
        Decodifica la instrucción y llena los campos según el opcode.
        Params:
        (Sin parámetros)
        Restriction:
        El texto debe estar validado y en formato correcto.
        Example:
            self._parse_instruction()
        """
        if not self.raw_text:
            return

        parts = self.raw_text.replace(',', '').split()
        if len(parts) == 0:
            return

        self.opcode = parts[0]
        self.operands = parts[1:]

        # Clasificación por opcode (simplificado)
        if self.opcode in {"add", "sub", "and", "or", "slt"}:
            self.type = InstructionType.R_TYPE
            self.rd, self.rs1, self.rs2 = self.operands

        elif self.opcode in {"addi", "andi", "ori", "slli", "srli"}:
            self.type = InstructionType.I_TYPE
            self.rd, self.rs1, imm = self.operands
            self.imm = int(imm)

        elif self.opcode in {"lw"}:
            self.type = InstructionType.I_TYPE
            self.rd, mem = self.operands
            # formato lw rd, imm(rs1)
            imm_part, rs1_part = mem.replace(')', '').split('(')
            self.rs1 = rs1_part
            self.imm = int(imm_part)

        elif self.opcode in {"sw"}:
            self.type = InstructionType.S_TYPE
            self.rs2, mem = self.operands
            imm_part, rs1_part = mem.replace(')', '').split('(')
            self.rs1 = rs1_part
            self.imm = int(imm_part)

        elif self.opcode in {"beq", "bne"}:
            self.type = InstructionType.B_TYPE
            self.rs1, self.rs2, imm = self.operands
            self.imm = int(imm)

        elif self.opcode in {"jal"}:
            self.type = InstructionType.J_TYPE
            self.rd, imm = self.operands
            self.imm = int(imm)

        else:
            self.type = InstructionType.INVALID

    def __str__(self):
        """
        Function: __str__
        Devuelve una representación textual de la instrucción con su dirección en hexadecimal.
        Returns:
        - str: representación de la instrucción.
        Example:
            print(instr)
        """
        return f"[{self.address:#04x}] {self.raw_text}"

    def is_valid(self):
        """
        Function: is_valid
        Indica si la instrucción es válida (no es de tipo INVALID).
        Returns:
        - bool: True si la instrucción es válida, False en caso contrario.
        Example:
            if instr.is_valid():
                ...
        """
        return self.type != InstructionType.INVALID
