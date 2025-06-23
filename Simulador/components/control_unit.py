class ControlUnit:
    def __init__(self):
        pass

    def generate_signals(self, opcode: str) -> dict:
        """
        Genera las señales de control para la instrucción dada por su opcode.
        """
        signals = {
            "RegWrite": False,
            "MemRead": False,
            "MemWrite": False,
            "MemToReg": False,
            "ALUSrc": False,
            "Branch": False,
            "ALUOp": "ADD"  # Por defecto
        }

        if opcode in {"add", "sub", "and", "or", "slt", "xor", "sll", "srl", "sra"}:
            signals["RegWrite"] = True
            signals["ALUSrc"] = False
            signals["ALUOp"] = opcode.upper()

        elif opcode in {"addi", "andi", "ori", "slti", "slli", "srli", "srai"}:
            signals["RegWrite"] = True
            signals["ALUSrc"] = True
            signals["ALUOp"] = opcode.upper()

        elif opcode == "lw":
            signals["RegWrite"] = True
            signals["MemRead"] = True
            signals["MemToReg"] = True
            signals["ALUSrc"] = True
            signals["ALUOp"] = "ADD"

        elif opcode == "sw":
            signals["MemWrite"] = True
            signals["ALUSrc"] = True
            signals["ALUOp"] = "ADD"

        elif opcode in {"beq", "bne", "blt", "bge", "bltu", "bgeu"}:
            signals["Branch"] = True
            signals["ALUOp"] = "SUB"

        elif opcode == "jal":
            signals["RegWrite"] = True
            signals["ALUOp"] = "ADD"  # Dirección de retorno en x[rd]

        elif opcode == "jalr":
            signals["RegWrite"] = True
            signals["ALUSrc"] = True
            signals["ALUOp"] = "ADD"

        elif opcode in {"lui", "auipc"}:
            signals["RegWrite"] = True
            signals["ALUSrc"] = True
            signals["ALUOp"] = "LUI" if opcode == "lui" else "AUIPC"

        elif opcode == "nop":
            pass  # todo en falso

        else:
            raise ValueError(f"Opcode no soportado: {opcode}")

        return signals
