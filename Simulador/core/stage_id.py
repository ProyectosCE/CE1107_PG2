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
from components.register_file import RegisterFile


"""
Class: InstructionDecode
Clase que representa la etapa de decodificación de instrucciones (ID) del pipeline, encargada de leer registros y extraer operandos.

Attributes:
- reg_file: RegisterFile - referencia al banco de registros para lectura de operandos.

Constructor:
- __init__: Recibe el banco de registros y lo almacena para uso en la decodificación.

Methods:
- decode: Decodifica la instrucción recibida desde IF/ID, lee los operandos y prepara los datos para la siguiente etapa.

Example:
    id_stage = InstructionDecode(reg_file)
    id_ex = id_stage.decode(if_id_dict)
"""

class InstructionDecode:
    def __init__(self, register_file: RegisterFile):
        """
        Function: __init__
        Inicializa la etapa de decodificación con una referencia al banco de registros.
        Params:
        - register_file: RegisterFile - banco de registros para lectura de operandos.
        Example:
            id_stage = InstructionDecode(reg_file)
        """
        self.reg_file = register_file

    def decode(self, if_id: dict) -> dict:
        """
        Function: decode
        Realiza la decodificación de la instrucción en IF/ID, leyendo los operandos del banco de registros.
        Params:
        - if_id: dict - diccionario con claves 'instr' y 'pc'.
        Returns:
        - dict: diccionario con los datos necesarios para la etapa EX (id_ex).
        Example:
            id_ex = id_stage.decode(if_id)
        """
        instr: Instruction = if_id["instr"]
        pc = if_id["pc"]

        # Si es NOP, simplemente propagar
        if instr.opcode == "nop":
            return {"instr": instr, "pc": pc}

        rs1_val = rs2_val = None

        if instr.rs1:
            rs1_val = self.reg_file.read(instr.rs1)
        if instr.rs2:
            rs2_val = self.reg_file.read(instr.rs2)

        return {
            "instr": instr,
            "pc": pc,
            "rs1_val": rs1_val,
            "rs2_val": rs2_val,
            "imm": instr.imm,
            "rd": instr.rd,
            "rs1": instr.rs1,
            "rs2": instr.rs2
        }
