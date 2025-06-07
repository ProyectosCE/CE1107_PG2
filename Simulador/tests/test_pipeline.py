import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.pipeline import Pipeline
from core.instruction import Instruction

def test_pipeline_shift():
    print("Probando avance del pipeline...")

    pipe = Pipeline()
    pipe.init_pipeline()

    instr1 = Instruction("add x1, x2, x3", 0)
    instr2 = Instruction("sub x4, x5, x6", 4)

    pipe.step(instr1, 0)
    state1 = pipe.dump_pipeline()
    assert state1["IF_ID"]["instr"].opcode == "add"
    assert state1["ID_EX"]["instr"].opcode == "nop"

    pipe.step(instr2, 4)
    state2 = pipe.dump_pipeline()
    assert state2["IF_ID"]["instr"].opcode == "sub"
    assert state2["ID_EX"]["instr"].opcode == "add"
    assert state2["EX_MEM"]["instr"].opcode == "nop"

    print("Test de avance del pipeline pasado correctamente.")

if __name__ == "__main__":
    test_pipeline_shift()
