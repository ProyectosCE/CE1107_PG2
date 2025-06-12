import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.hazard_unit import HazardUnit
from core.instruction import Instruction

def test_no_hazard():
    print("Test: sin hazards")
    hu = HazardUnit()

    instr_id = Instruction("add x5, x1, x2", 0)
    instr_ex = Instruction("sub x3, x4, x6", 4)
    instr_mem = Instruction("or x7, x8, x9", 8)
    instr_wb = Instruction("and x10, x11, x12", 12)

    result = hu.detect_hazard(
        {"instr": instr_id},
        {"instr": instr_ex},
        {"instr": instr_mem},
        {"instr": instr_wb}
    )

    assert result["stall"] is False
    assert result["forward"] == {'rs1': None, 'rs2': None}
    print("Test sin hazards pasó.")

def test_load_use_hazard():
    print("Test: load-use hazard (stall)")
    hu = HazardUnit()

    instr_id = Instruction("add x5, x1, x2", 0)     # Usa x1, x2
    instr_ex = Instruction("lw x1, 0(x3)", 4)       # x1 aún no escrito

    result = hu.detect_hazard(
        {"instr": instr_id},
        {"instr": instr_ex},
        {"instr": None},
        {"instr": None}
    )

    assert result["stall"] is True
    print("Test load-use hazard (stall) pasó.")

def test_forward_from_ex():
    print("Test: forwarding desde EX/MEM")
    hu = HazardUnit()

    instr_id = Instruction("sub x5, x1, x2", 0)     # Usa x1, x2
    instr_ex = Instruction("add x6, x7, x8", 4)
    instr_mem = Instruction("add x1, x9, x10", 8)   # Produce x1
    instr_wb = Instruction("add x11, x12, x13", 12)

    result = hu.detect_hazard(
        {"instr": instr_id},
        {"instr": instr_ex},
        {"instr": instr_mem},
        {"instr": instr_wb}
    )

    assert result["stall"] is False
    assert result["forward"]['rs1'] == 'EX'
    assert result["forward"]['rs2'] is None
    print("Test forwarding desde EX/MEM pasó.")

def test_forward_from_mem():
    print("Test: forwarding desde MEM/WB")
    hu = HazardUnit()

    instr_id = Instruction("sub x5, x1, x2", 0)
    instr_mem = Instruction("add x6, x7, x8", 8)
    instr_wb = Instruction("add x2, x9, x10", 12)

    result = hu.detect_hazard(
        {"instr": instr_id},
        {"instr": Instruction("add x4, x3, x3", 4)},
        {"instr": instr_mem},
        {"instr": instr_wb}
    )

    assert result["forward"]['rs2'] == 'MEM'
    print("Test forwarding desde MEM/WB pasó.")

def test_ignore_x0():
    print("Test: ignorar registros x0")
    hu = HazardUnit()

    instr_id = Instruction("add x1, x0, x0", 0)  # usa x0, x0
    instr_ex = Instruction("lw x0, 0(x3)", 4)    # escribe en x0 (no permitido)
    instr_mem = Instruction("add x0, x0, x0", 8)
    instr_wb = Instruction("add x0, x0, x0", 12)

    result = hu.detect_hazard(
        {"instr": instr_id},
        {"instr": instr_ex},
        {"instr": instr_mem},
        {"instr": instr_wb}
    )

    assert result["stall"] is False
    assert result["forward"] == {'rs1': None, 'rs2': None}
    print("Test ignorar x0 pasó.")

if __name__ == "__main__":
    test_no_hazard()
    test_load_use_hazard()
    test_forward_from_ex()
    test_forward_from_mem()
    test_ignore_x0()
