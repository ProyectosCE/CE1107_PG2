"""
================================== LICENCIA ==============================
MIT License
Copyright (c) 2025 José Bernardo Barquero Bonilla,
Jose Eduardo Campos Salazar,
Jimmy Feng Feng,
Alexander Montero Vargas
Consulta el archivo LICENSE para más detalles.
==========================================================================
"""

"""
Este módulo realiza pruebas unitarias para el parser de instrucciones, validando el reconocimiento de etiquetas,
la cantidad de instrucciones y la correcta decodificación de los opcodes.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from io.parser import Parser

def test_simple_program():
    """
    Function: test_simple_program
    Prueba el parser con un programa simple que incluye etiquetas y diferentes tipos de instrucciones.
    Example:
        test_simple_program()
    """
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
