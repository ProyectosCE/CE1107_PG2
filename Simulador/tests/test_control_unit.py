import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.control_unit import ControlUnit

def test_add_instruction():
    cu = ControlUnit()
    signals = cu.generate_signals("add")
    assert signals["RegWrite"] is True
    assert signals["ALUSrc"] is False
    assert signals["ALUOp"] == "ADD"

def test_lw_instruction():
    cu = ControlUnit()
    signals = cu.generate_signals("lw")
    assert signals["RegWrite"] is True
    assert signals["MemRead"] is True
    assert signals["MemToReg"] is True
    assert signals["ALUSrc"] is True
    assert signals["ALUOp"] == "ADD"

def test_sw_instruction():
    cu = ControlUnit()
    signals = cu.generate_signals("sw")
    assert signals["RegWrite"] is False
    assert signals["MemWrite"] is True
    assert signals["ALUSrc"] is True

def test_branch_instruction():
    cu = ControlUnit()
    signals = cu.generate_signals("beq")
    assert signals["Branch"] is True
    assert signals["ALUOp"] == "SUB"

def test_jal_instruction():
    cu = ControlUnit()
    signals = cu.generate_signals("jal")
    assert signals["RegWrite"] is True
    assert signals["ALUOp"] == "ADD"

def test_invalid_instruction():
    cu = ControlUnit()
    try:
        cu.generate_signals("illegal")
    except ValueError as e:
        assert "Opcode no soportado" in str(e)
    else:
        assert False, "Se esperaba una excepción por opcode inválido"

if __name__ == "__main__":
    print("Ejecutando pruebas para la unidad de control...")
    test_add_instruction()
    test_lw_instruction()
    test_sw_instruction()
    test_branch_instruction()
    test_jal_instruction()
    test_invalid_instruction()
    print("Todas las pruebas pasaron correctamente.")
