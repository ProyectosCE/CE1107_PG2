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
from components.branch_predictor import BranchPredictor

class InstructionDecode:
    def __init__(self, register_file: RegisterFile, branch_predictor: BranchPredictor):
        """
        Inicializa la etapa de decodificación con referencias al banco de registros
        y al predictor de saltos.
        """
        self.reg_file = register_file
        self.branch_predictor = branch_predictor

    def decode(self, if_id: dict) -> dict:
        """
        Realiza la decodificación de la instrucción en IF/ID, leyendo los operandos
        del banco de registros y consultando el predictor de saltos si aplica.
        """
        instr: Instruction = if_id["instr"]
        pc = if_id["pc"]

        if instr.opcode == "nop":
            return {"instr": instr, "pc": pc}

        rs1_val = self.reg_file.read(instr.rs1) if instr.rs1 else None
        rs2_val = self.reg_file.read(instr.rs2) if instr.rs2 else None

        id_ex = {
            "instr": instr,
            "pc": pc,
            "rs1_val": rs1_val,
            "rs2_val": rs2_val,
            "imm": instr.imm,
            "rd": instr.rd,
            "rs1": instr.rs1,
            "rs2": instr.rs2
        }

        # Predicción de saltos
        if instr.opcode in {"beq", "bne", "jal"}:
            prediction = self.branch_predictor.predict(pc)
            id_ex["predicted_taken"] = prediction["taken"]

            if prediction["taken"]:
                id_ex["predicted_target"] = pc + instr.imm
            else:
                id_ex["predicted_target"] = pc + 4  # flujo secuencial

        return id_ex
