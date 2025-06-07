class ExecuteStage:
    def __init__(self):
        pass

    def execute(self, id_ex: dict) -> dict:
        """
        Ejecuta la instrucción usando ALU y calcula resultados.

        Entrada:
        - id_ex: dict generado por la etapa ID

        Salida:
        - ex_mem: dict con:
            - 'instr', 'alu_result', 'rs2_val'
            - 'rd', 'pc', 'branch_taken', 'target_address'
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
            alu_result = rs1_val + imm  # Dirección efectiva
        elif opcode == "beq":
            branch_taken = rs1_val == rs2_val
            target_address = pc + imm
        elif opcode == "bne":
            branch_taken = rs1_val != rs2_val
            target_address = pc + imm
        elif opcode == "jal":
            alu_result = pc + 4  # return address
            target_address = pc + imm
            branch_taken = True
        elif opcode == "nop":
            pass  # No operación
        else:
            raise ValueError(f"Operación no soportada: {opcode}")

        return {
            "instr": instr,
            "alu_result": alu_result,
            "rs2_val": rs2_val,
            "rd": id_ex.get("rd"),
            "pc": pc,
            "branch_taken": branch_taken,
            "target_address": target_address
        }
