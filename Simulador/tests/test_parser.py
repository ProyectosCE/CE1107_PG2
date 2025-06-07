import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from IO.parser import Parser

def test_simple_program():
    program = [
        "start: add x1, x0, x0",
        "addi x2, x1, 10",
        "loop: beq x2, x0, end",
        "addi x2, x2, -1",
        "jal x0, loop",
        "end: sw x1, 0(x2)"
    ]

    parser = Parser()
    instrs = parser.parse(program)

    print(len(instrs))  # → Debería ser 6
    assert len(instrs) == 6
    assert instrs[0].opcode == "add"
    assert instrs[-1].opcode == "sw"


if __name__ == "__main__":
    print("Probando el parser de instrucciones...")
    test_simple_program()
    print("Todas las pruebas pasaron correctamente.")
