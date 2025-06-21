"""
ExecuteStageBasic: Etapa EX sin predicción de saltos
"""

class ExecuteStageBasic:
    def __init__(self):
        """
        Versión básica de la etapa EX: sin lógica de predicción de saltos.
        """
        pass

    def execute(self, id_ex: dict) -> dict:
        instr = id_ex["instr"]
        opcode = instr.opcode

        alu_result = 0
        branch_taken = False
        target_address = None

        rs1_val = id_ex.get("rs1_val", 0)
        rs2_val = id_ex.get("rs2_val", 0)
        imm = id_ex.get("imm", 0)
        pc = id_ex["pc"]

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
        elif opcode in {"lw", "sw"}:
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

        return {
            "instr": instr,
            "alu_result": alu_result,
            "rs2_val": rs2_val,
            "rd": id_ex.get("rd"),
            "pc": pc,
            "branch_taken": branch_taken,
            "target_address": target_address,
            "flush_required": False  
        }
