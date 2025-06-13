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

        if opcode == "add" or opcode == "sub" or opcode == "and" or opcode == "or" or opcode == "slt":
            signals["RegWrite"] = True
            signals["ALUSrc"] = False
            signals["ALUOp"] = opcode.upper()

        elif opcode == "addi":
            signals["RegWrite"] = True
            signals["ALUSrc"] = True
            signals["ALUOp"] = "ADD"

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

        elif opcode == "beq" or opcode == "bne":
            signals["Branch"] = True
            signals["ALUOp"] = "SUB"

        elif opcode == "jal":
            signals["RegWrite"] = True
            signals["ALUOp"] = "ADD"  # Dirección de retorno en x[rd]

        elif opcode == "nop":
            pass  # todo en falso

        else:
            raise ValueError(f"Opcode no soportado: {opcode}")

        return signals
