from core.instruction import Instruction
from components.register_file import RegisterFile


class InstructionDecode:
    def __init__(self, register_file: RegisterFile):
        self.reg_file = register_file

    def decode(self, if_id: dict) -> dict:
        """
        Realiza la decodificación de la instrucción en IF/ID.

        Entrada:
        - if_id: dict con claves 'instr' y 'pc'

        Salida:
        - id_ex: dict con:
            - 'instr'
            - 'pc'
            - 'rs1_val', 'rs2_val'
            - 'imm'
            - 'rd', 'rs1', 'rs2'
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
