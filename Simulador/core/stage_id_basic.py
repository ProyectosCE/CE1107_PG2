"""
InstructionDecodeBasic: Versión simplificada de la etapa ID
Sin predicción de saltos ni unidad de control
"""

from core.instruction import Instruction
from components.register_file import RegisterFile
import time
from config import LATENCY_ID

class InstructionDecodeBasic:
    def __init__(self, register_file: RegisterFile, latency: float = None):
        """
        Inicializa la etapa ID solo con acceso al banco de registros.
        """
        self.reg_file = register_file
        self.latency = latency if latency is not None else LATENCY_ID

    def decode(self, if_id: dict) -> dict:
        """
        Decodifica la instrucción y lee los valores de los registros fuente.
        No aplica predicción de saltos ni control.
        """
        instr: Instruction = if_id["instr"]
        pc = if_id["pc"]

        if instr.opcode == "nop":
            return {"instr": instr, "pc": pc}

        rs1_val = self.reg_file.read(instr.rs1) if instr.rs1 else 0
        rs2_val = self.reg_file.read(instr.rs2) if instr.rs2 else 0

        time.sleep(self.latency)
        return {
            "instr": instr,
            "pc": pc,
            "rs1_val": rs1_val,
            "rs2_val": rs2_val,
            "imm": instr.imm,
            "rd": instr.rd,
            "rs1": instr.rs1,
            "rs2": instr.rs2,
            # "control_signals": {}  # Si quieres agregar señales de control aquí
        }
