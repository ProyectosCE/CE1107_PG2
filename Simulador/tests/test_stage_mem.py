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
Este módulo realiza pruebas unitarias para la etapa de acceso a memoria (MEM) del pipeline,
validando operaciones de carga (lw) y almacenamiento (sw).
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.stage_mem import MemoryAccessStage
from components.memory import Memory
from core.instruction import Instruction

def test_lw_access():
    """
    Function: test_lw_access
    Prueba la operación de carga (lw) en la etapa MEM.
    Example:
        test_lw_access()
    """
    mem = Memory()
    mem.store_word(12, 999)

    stage = MemoryAccessStage(mem)
    instr = Instruction("lw x1, 8(x2)", 0)

    ex_mem = {
        "instr": instr,
        "rd": "x1",
        "alu_result": 12,
        "pc": 0
    }

    result = stage.access(ex_mem)
    assert result["mem_data"] == 999
    print("Test lw pasó correctamente.")

def test_sw_access():
    """
    Function: test_sw_access
    Prueba la operación de almacenamiento (sw) en la etapa MEM.
    Example:
        test_sw_access()
    """
    mem = Memory()
    stage = MemoryAccessStage(mem)

    instr = Instruction("sw x3, 0(x2)", 0)

    ex_mem = {
        "instr": instr,
        "rd": None,
        "alu_result": 16,
        "rs2_val": 1234,
        "pc": 0
    }

    result = stage.access(ex_mem)
    assert mem.load_word(16) == 1234
    print("Test sw pasó correctamente.")

if __name__ == "__main__":
    test_lw_access()
    test_sw_access()
