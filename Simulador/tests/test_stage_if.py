import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.stage_if import InstructionFetch
from components.memory import Memory
from core.instruction import Instruction

def test_instruction_fetch():
    print("Probando Instruction Fetch...")

    # Crear memoria con instrucciones
    instr_mem = Memory()
    instr_mem.store_word(0, Instruction("add x1, x2, x3", 0))
    instr_mem.store_word(4, Instruction("sub x4, x5, x6", 4))
    instr_mem.store_word(8, Instruction("addi x7, x0, 10", 8))

    if_stage = InstructionFetch(instr_mem)

    # Primer ciclo
    res1 = if_stage.fetch()
    assert res1["instr"].opcode == "add"
    assert res1["pc"] == 0

    # Segundo ciclo
    res2 = if_stage.fetch()
    assert res2["instr"].opcode == "sub"
    assert res2["pc"] == 4

    # Tercer ciclo
    res3 = if_stage.fetch()
    assert res3["instr"].opcode == "addi"
    assert res3["pc"] == 8

    print("Instruction Fetch pasó la prueba.")

if __name__ == "__main__":
    test_instruction_fetch()
