from components.branch_predictor import BranchPredictor
import time
from config import LATENCY_EX

class ExecuteStage:
    def __init__(self, branch_predictor: BranchPredictor, latency: float = None):
        self.branch_predictor = branch_predictor
        self.latency = latency if latency is not None else LATENCY_EX

    def execute(self, id_ex: dict) -> dict:
        instr = id_ex["instr"]
        opcode = instr.opcode

        control = id_ex.get("control_signals", {})

        alu_result = 0
        branch_taken = False
        target_address = None
        flush_required = False

        rs1_val = id_ex.get("rs1_val", 0)
        rs2_val = id_ex.get("rs2_val", 0)
        imm = id_ex.get("imm", 0)
        pc = id_ex["pc"]

        # Decidir segundo operando ALU (inmediato o registro)
        operand2 = imm if control.get("ALUSrc", False) else rs2_val

        # Ejecutar operación según ALUOp
        alu_op = control.get("ALUOp", "ADD")

        if alu_op == "ADD":
            alu_result = rs1_val + operand2
        elif alu_op == "SUB":
            alu_result = rs1_val - operand2
        elif alu_op == "AND":
            alu_result = rs1_val & operand2
        elif alu_op == "OR":
            alu_result = rs1_val | operand2
        elif alu_op == "XOR":
            alu_result = rs1_val ^ operand2
        elif alu_op == "SLT":
            alu_result = int(rs1_val < operand2)
        elif alu_op == "SLL":
            alu_result = rs1_val << (operand2 & 0x1F)
        elif alu_op == "SRL":
            alu_result = (rs1_val % (1 << 32)) >> (operand2 & 0x1F)
        elif alu_op == "SRA":
            alu_result = rs1_val >> (operand2 & 0x1F)
        elif alu_op == "ADDI":
            alu_result = rs1_val + imm
        elif alu_op == "ANDI":
            alu_result = rs1_val & imm
        elif alu_op == "ORI":
            alu_result = rs1_val | imm
        elif alu_op == "SLTI":
            alu_result = int(rs1_val < imm)
        elif alu_op == "SLLI":
            alu_result = rs1_val << (imm & 0x1F)
        elif alu_op == "SRLI":
            alu_result = (rs1_val % (1 << 32)) >> (imm & 0x1F)
        elif alu_op == "SRAI":
            alu_result = rs1_val >> (imm & 0x1F)
        elif alu_op == "LUI":
            alu_result = imm << 12
        elif alu_op == "AUIPC":
            alu_result = pc + (imm << 12)
        elif alu_op == "NOP":
            pass
        else:
            raise ValueError(f"ALUOp no soportado: {alu_op}")

        # Lógica de branch extendida
        if opcode == "beq":
            branch_taken = rs1_val == rs2_val
            target_address = pc + imm
        elif opcode == "bne":
            branch_taken = rs1_val != rs2_val
            target_address = pc + imm
        elif opcode == "blt":
            branch_taken = rs1_val < rs2_val
            target_address = pc + imm
        elif opcode == "bge":
            branch_taken = rs1_val >= rs2_val
            target_address = pc + imm
        elif opcode == "bltu":
            branch_taken = (rs1_val & 0xFFFFFFFF) < (rs2_val & 0xFFFFFFFF)
            target_address = pc + imm
        elif opcode == "bgeu":
            branch_taken = (rs1_val & 0xFFFFFFFF) >= (rs2_val & 0xFFFFFFFF)
            target_address = pc + imm
        elif opcode == "jal":
            alu_result = pc + 4
            target_address = pc + imm
            branch_taken = True
        elif opcode == "jalr":
            alu_result = pc + 4
            target_address = (rs1_val + imm) & ~1
            branch_taken = True

        # Verificación de predicción de salto
        if opcode in {"beq", "bne", "jal"}:
            predicted = id_ex.get("predicted_taken", False)
            actual = branch_taken
            self.branch_predictor.update(pc, actual)

            if self.branch_predictor.flush_required(predicted, actual):
                flush_required = True
                print(f"Predicción incorrecta @ PC={pc} → FLUSH requerido")

        time.sleep(self.latency)
        return {
            "instr": instr,
            "alu_result": alu_result,
            "rs2_val": rs2_val,
            "rd": id_ex.get("rd"),
            "pc": pc,
            "branch_taken": branch_taken,
            "target_address": target_address,
            "flush_required": flush_required,
            "control_signals": control  # Propagar señales a MEM
        }
