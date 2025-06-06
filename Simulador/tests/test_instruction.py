import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.instruction import Instruction, InstructionType

# Este módulo realiza pruebas unitarias para la clase Instruction, para así validar de que está funcionando correctamente

def test_r_type():
    instr = Instruction("add x1, x2, x3", 0)
    assert instr.opcode == "add"
    assert instr.rd == "x1"
    assert instr.rs1 == "x2"
    assert instr.rs2 == "x3"
    assert instr.type == InstructionType.R_TYPE
    assert instr.is_valid()


def test_i_type_addi():
    instr = Instruction("addi x4, x5, 10", 4)
    assert instr.opcode == "addi"
    assert instr.rd == "x4"
    assert instr.rs1 == "x5"
    assert instr.imm == 10
    assert instr.type == InstructionType.I_TYPE
    assert instr.is_valid()


def test_i_type_lw():
    instr = Instruction("lw x6, 8(x7)", 8)
    assert instr.opcode == "lw"
    assert instr.rd == "x6"
    assert instr.rs1 == "x7"
    assert instr.imm == 8
    assert instr.type == InstructionType.I_TYPE
    assert instr.is_valid()


def test_s_type_sw():
    instr = Instruction("sw x8, 12(x9)", 12)
    assert instr.opcode == "sw"
    assert instr.rs2 == "x8"
    assert instr.rs1 == "x9"
    assert instr.imm == 12
    assert instr.type == InstructionType.S_TYPE
    assert instr.is_valid()


def test_b_type_beq():
    instr = Instruction("beq x10, x11, 16", 16)
    assert instr.opcode == "beq"
    assert instr.rs1 == "x10"
    assert instr.rs2 == "x11"
    assert instr.imm == 16
    assert instr.type == InstructionType.B_TYPE
    assert instr.is_valid()


def test_j_type_jal():
    instr = Instruction("jal x1, 100", 100)
    assert instr.opcode == "jal"
    assert instr.rd == "x1"
    assert instr.imm == 100
    assert instr.type == InstructionType.J_TYPE
    assert instr.is_valid()


def test_invalid_instruction():
    instr = Instruction("foobar x1, x2, x3", 0)
    assert instr.type == InstructionType.INVALID
    assert not instr.is_valid()


if __name__ == "__main__":
    print("Pruebas de instrucciones:")
    test_r_type()
    test_i_type_addi()
    test_i_type_lw()
    test_s_type_sw()
    test_b_type_beq()
    test_j_type_jal()
    test_invalid_instruction()
    print("Todas las pruebas pasaron correctamente.")
