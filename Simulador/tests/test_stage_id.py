import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.stage_id import InstructionDecode
from components.register_file import RegisterFile
from core.instruction import Instruction


def test_instruction_decode():
    print(" Probando Instruction Decode (ID)...")

    # Crear banco de registros
    rf = RegisterFile()
    rf.write("x2", 10)
    rf.write("x3", 20)

    # Crear una instrucción tipo R
    instr = Instruction("add x1, x2, x3", 0)

    # Simular IF/ID register
    if_id = {
        "instr": instr,
        "pc": 0
    }

    # Crear etapa ID y decodificar
    id_stage = InstructionDecode(rf)
    id_ex = id_stage.decode(if_id)

    # Validar resultados
    assert id_ex["rs1_val"] == 10
    assert id_ex["rs2_val"] == 20
    assert id_ex["rd"] == "x1"
    assert id_ex["rs1"] == "x2"
    assert id_ex["rs2"] == "x3"
    assert id_ex["pc"] == 0
    assert id_ex["instr"].opcode == "add"

    print(" Instruction Decode pasó la prueba correctamente.")

if __name__ == "__main__":
    test_instruction_decode()
