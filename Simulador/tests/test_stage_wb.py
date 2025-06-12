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
Este módulo realiza pruebas unitarias para la etapa de escritura final (WB) del pipeline,
validando la correcta escritura en el banco de registros y el comportamiento ante instrucciones que no deben escribir.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.stage_wb import WriteBackStage
from components.register_file import RegisterFile
from core.instruction import Instruction

def test_writeback_lw():
    """
    Function: test_writeback_lw
    Prueba la escritura de un valor cargado desde memoria (lw) en el banco de registros.
    Example:
        test_writeback_lw()
    """
    rf = RegisterFile()
    wb = WriteBackStage(rf)

    instr = Instruction("lw x1, 0(x2)", 0)
    mem_wb = {
        "instr": instr,
        "rd": "x1",
        "mem_data": 999
    }

    wb.write_back(mem_wb)
    assert rf.read("x1") == 999
    print("Test lw pasó correctamente.")

def test_writeback_add():
    """
    Function: test_writeback_add
    Prueba la escritura del resultado de una operación aritmética (add) en el banco de registros.
    Example:
        test_writeback_add()
    """
    rf = RegisterFile()
    wb = WriteBackStage(rf)

    instr = Instruction("add x5, x1, x2", 0)
    mem_wb = {
        "instr": instr,
        "rd": "x5",
        "alu_result": 123
    }

    wb.write_back(mem_wb)
    assert rf.read("x5") == 123
    print("Test add pasó correctamente.")

def test_writeback_sw_ignored():
    """
    Function: test_writeback_sw_ignored
    Prueba que una instrucción sw no escriba en el banco de registros.
    Example:
        test_writeback_sw_ignored()
    """
    rf = RegisterFile()
    rf.write("x3", 777)

    wb = WriteBackStage(rf)
    instr = Instruction("sw x3, 0(x2)", 0)
    mem_wb = {
        "instr": instr,
        "rd": None,
        "alu_result": 0
    }

    wb.write_back(mem_wb)
    assert rf.read("x3") == 777  # No cambia
    print("Test sw no escribió en registros (correctamente).")

if __name__ == "__main__":
    test_writeback_lw()
    test_writeback_add()
    test_writeback_sw_ignored()
