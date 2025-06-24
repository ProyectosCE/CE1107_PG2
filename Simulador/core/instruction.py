from enum import Enum, auto
class InstructionType(Enum):
    R_TYPE = auto()
    I_TYPE = auto()
    S_TYPE = auto()
    B_TYPE = auto()
    J_TYPE = auto()
    U_TYPE = auto()
    INVALID = auto()

class Instruction:
    def __init__(self, raw_text: str, address: int):
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
        
        if not self.raw_text:
            return

        parts = self.raw_text.replace(',', '').split()
        if len(parts) == 0:
            return

        self.opcode = parts[0]
        self.operands = parts[1:]

        # Clasificación por opcode (ampliada, solo lw/sw para memoria)
        if self.opcode in {"add", "sub", "and", "or", "slt", "xor", "sll", "srl", "sra"}:
            self.type = InstructionType.R_TYPE
            self.rd, self.rs1, self.rs2 = self.operands

        elif self.opcode in {"addi", "andi", "ori", "slti", "slli", "srli", "srai"}:
            self.type = InstructionType.I_TYPE
            self.rd, self.rs1, imm = self.operands
            self.imm = int(imm)

        elif self.opcode == "lw":
            self.type = InstructionType.I_TYPE
            self.rd, mem = self.operands
            # formato lw rd, imm(rs1)
            imm_part, rs1_part = mem.replace(')', '').split('(')
            self.rs1 = rs1_part
            self.imm = int(imm_part)

        elif self.opcode == "sw":
            self.type = InstructionType.S_TYPE
            self.rs2, mem = self.operands
            imm_part, rs1_part = mem.replace(')', '').split('(')
            self.rs1 = rs1_part
            self.imm = int(imm_part)

        elif self.opcode in {"beq", "bne", "blt", "bge", "bltu", "bgeu"}:
            self.type = InstructionType.B_TYPE
            self.rs1, self.rs2, imm = self.operands
            self.imm = int(imm)

        elif self.opcode in {"jal"}:
            self.type = InstructionType.J_TYPE
            self.rd, imm = self.operands
            self.imm = int(imm)

        elif self.opcode in {"jalr"}:
            self.type = InstructionType.I_TYPE
            self.rd, mem = self.operands
            # formato jalr rd, imm(rs1)
            imm_part, rs1_part = mem.replace(')', '').split('(')
            self.rs1 = rs1_part
            self.imm = int(imm_part)

        elif self.opcode in {"lui", "auipc"}:
            self.type = InstructionType.U_TYPE
            self.rd, imm = self.operands
            self.imm = int(imm)

        else:
            self.type = InstructionType.INVALID

    def __str__(self):
        return f"[{self.address:#04x}] {self.raw_text}"

    def is_valid(self):
        return self.type != InstructionType.INVALID
