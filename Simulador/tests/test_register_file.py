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
Este módulo realiza pruebas unitarias para la clase RegisterFile, validando operaciones de lectura, escritura,
comportamiento especial del registro x0, reinicio y manejo de registros inválidos.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.register_file import RegisterFile

def test_basic_rw():
    """
    Function: test_basic_rw
    Prueba la escritura y lectura básica en un registro distinto de x0.
    Example:
        test_basic_rw()
    """
    rf = RegisterFile()
    rf.write("x1", 10)
    assert rf.read("x1") == 10

def test_x0_behavior():
    """
    Function: test_x0_behavior
    Prueba que el registro x0 siempre retorne 0, incluso tras intentar escribirle.
    Example:
        test_x0_behavior()
    """
    rf = RegisterFile()
    rf.write("x0", 999)
    assert rf.read("x0") == 0

def test_reset():
    """
    Function: test_reset
    Prueba que el método reset reinicie todos los registros (excepto x0) a 0.
    Example:
        test_reset()
    """
    rf = RegisterFile()
    rf.write("x3", 77)
    rf.reset()
    assert rf.read("x3") == 0

def test_invalid_register():
    """
    Function: test_invalid_register
    Prueba que se lance un error al intentar acceder a un registro inválido.
    Example:
        test_invalid_register()
    """
    rf = RegisterFile()
    try:
        rf.read("x33")
        assert False, "Expected ValueError for x33"
    except ValueError:
        pass

if __name__ == "__main__":
    print("Probando RegisterFile...")
    test_basic_rw()
    test_x0_behavior()
    test_reset()
    test_invalid_register()
    print("Todos los tests pasaron correctamente.")
