import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from InOut.parser import Parser

def test_simple_program():
    print("🔹 Test: programa válido con etiquetas y saltos")
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

    assert len(instrs) == 6
    assert instrs[0].opcode == "add"
    assert instrs[-1].opcode == "sw"
    print("Test pasado.")

def test_invalid_operand_count():
    print("Test: instrucción con operandos faltantes (error esperado)")
    program = [
        "add x1, x2"  # Faltante rs2
    ]
    parser = Parser()
    try:
        parser.parse(program)
    except ValueError as e:
        print(f"Error detectado correctamente: {e}")
    else:
        assert False, "Error esperado pero no lanzado."

def test_undefined_label():
    print("🔹 Test: salto a etiqueta no definida (error esperado)")
    program = [
        "beq x1, x2, not_defined"
    ]
    parser = Parser()
    try:
        parser.parse(program)
    except ValueError as e:
        print(f"Error detectado correctamente: {e}")
    else:
        assert False, "Error esperado pero no lanzado."

def test_invalid_instruction():
    print("Test: instrucción inválida (error esperado)")
    program = [
        "foo x1, x2, x3"  # No existe el opcode
    ]
    parser = Parser()
    try:
        parser.parse(program)
    except ValueError as e:
        print(f"Error detectado correctamente: {e}")
    else:
        assert False, "Error esperado pero no lanzado."

if __name__ == "__main__":
    print("Iniciando pruebas para el parser...\n")
    test_simple_program()
    print()
    test_invalid_operand_count()
    print()
    test_undefined_label()
    print()
    test_invalid_instruction()
    print("\n Todas las pruebas pasaron correctamente.")
