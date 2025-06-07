import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.stage_ex import ExecuteStage
from core.instruction import Instruction

def test_execute_add():
    ex = ExecuteStage()

    instr = Instruction("add x1, x2, x3", 0)
    id_ex = {
        "instr": instr,
        "rs1_val": 10,
        "rs2_val": 20,
        "pc": 0,
        "rd": "x1"
    }

    result = ex.execute(id_ex)
    assert result["alu_result"] == 30
    assert result["rd"] == "x1"
    assert result["branch_taken"] is False
    print("Test add pasó correctamente.")

def test_execute_beq_taken():
    ex = ExecuteStage()

    instr = Instruction("beq x1, x2, 8", 4)
    id_ex = {
        "instr": instr,
        "rs1_val": 5,
        "rs2_val": 5,
        "pc": 4,
        "imm": instr.imm,
    }
    result = ex.execute(id_ex)
    assert result["branch_taken"] is True
    


    assert result["target_address"] == 12
    print("Test beq tomado pasó correctamente.")

def test_execute_jal():
    ex = ExecuteStage()

    instr = Instruction("jal x5, 12", 8)

    id_ex = {
        "instr": instr,
        "pc": 8,
        "rd": "x5",
        "imm": instr.imm,
    }


    result = ex.execute(id_ex)
    assert result["alu_result"] == 12  # return address = pc + 4
    assert result["target_address"] == 20  # pc + imm
    assert result["branch_taken"] is True
    print("Test jal pasó correctamente.")

if __name__ == "__main__":
    test_execute_add()
    test_execute_beq_taken()
    test_execute_jal()
