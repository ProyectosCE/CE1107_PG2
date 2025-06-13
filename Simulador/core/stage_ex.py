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

from components.branch_predictor import BranchPredictor

class ExecuteStage:
    def __init__(self, branch_predictor: BranchPredictor):
        """
        Inicializa la etapa EX con acceso al predictor de saltos.
        """
        self.branch_predictor = branch_predictor

    def execute(self, id_ex: dict) -> dict:
        """
        Ejecuta la instrucción usando la ALU y controla lógica de saltos.
        """
        instr = id_ex["instr"]
        opcode = instr.opcode

        alu_result = 0
        branch_taken = False
        target_address = None

        rs1_val = id_ex.get("rs1_val", 0)
        rs2_val = id_ex.get("rs2_val", 0)
        imm = id_ex.get("imm", 0)
        pc = id_ex["pc"]

        # ALU y lógica de saltos
        if opcode == "add":
            alu_result = rs1_val + rs2_val
        elif opcode == "sub":
            alu_result = rs1_val - rs2_val
        elif opcode == "and":
            alu_result = rs1_val & rs2_val
        elif opcode == "or":
            alu_result = rs1_val | rs2_val
        elif opcode == "slt":
            alu_result = int(rs1_val < rs2_val)
        elif opcode == "addi":
            alu_result = rs1_val + imm
        elif opcode == "lw" or opcode == "sw":
            alu_result = rs1_val + imm
        elif opcode == "beq":
            branch_taken = rs1_val == rs2_val
            target_address = pc + imm
        elif opcode == "bne":
            branch_taken = rs1_val != rs2_val
            target_address = pc + imm
        elif opcode == "jal":
            alu_result = pc + 4
            target_address = pc + imm
            branch_taken = True
        elif opcode == "nop":
            pass
        else:
            raise ValueError(f"Operación no soportada: {opcode}")

        # Validar predicción (solo si es instrucción de salto)
        flush_required = False
        if opcode in {"beq", "bne", "jal"}:
            predicted = id_ex.get("predicted_taken", False)
            actual = branch_taken

            self.branch_predictor.update(pc, actual)

            if self.branch_predictor.flush_required(predicted, actual):
                flush_required = True
                print(f" Predicción incorrecta @ PC={pc} → FLUSH requerido")

        return {
            "instr": instr,
            "alu_result": alu_result,
            "rs2_val": rs2_val,
            "rd": id_ex.get("rd"),
            "pc": pc,
            "branch_taken": branch_taken,
            "target_address": target_address,
            "flush_required": flush_required
        }
