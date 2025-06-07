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
Este módulo realiza pruebas unitarias para la clase Memory, validando operaciones de lectura, escritura,
manejo de errores por direcciones desalineadas y fuera de rango, y carga de programas.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.memory import Memory

def test_basic_rw():
    """
    Function: test_basic_rw
    Prueba operaciones básicas de escritura y lectura en memoria.
    Example:
        test_basic_rw()
    """
    mem = Memory(4)
    mem.store_word(0, 123)
    mem.store_word(4, 456)
    assert mem.load_word(0) == 123
    assert mem.load_word(4) == 456

def test_unaligned_access():
    """
    Function: test_unaligned_access
    Prueba que se lance un error al intentar acceder a una dirección desalineada.
    Example:
        test_unaligned_access()
    """
    mem = Memory(4)
    try:
        mem.store_word(3, 99)
        assert False, "Expected ValueError for unaligned address"
    except ValueError:
        pass

def test_out_of_bounds():
    """
    Function: test_out_of_bounds
    Prueba que se lance un error al intentar acceder a una dirección fuera de rango.
    Example:
        test_out_of_bounds()
    """
    mem = Memory(4)
    try:
        mem.store_word(4096, 10)  # 4*1024 = 4096, fuera de rango
        assert False, "Expected ValueError for out of range"
    except ValueError:
        pass

def test_load_program():
    """
    Function: test_load_program
    Prueba la carga de un bloque de datos en memoria usando load_program.
    Example:
        test_load_program()
    """
    mem = Memory(4)
    mem.load_program([10, 20, 30])
    assert mem.load_word(0) == 10
    assert mem.load_word(4) == 20
    assert mem.load_word(8) == 30

if __name__ == "__main__":
    print("Probando memoria...")
    test_basic_rw()
    test_unaligned_access()
    test_out_of_bounds()
    test_load_program()
    print("Todas las pruebas pasaron correctamente.")
