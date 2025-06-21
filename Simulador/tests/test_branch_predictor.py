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
Este módulo realiza pruebas unitarias para la clase BranchPredictor, validando la predicción por defecto,
la actualización de la predicción, y la detección de necesidad de flush por predicción errónea.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from components.branch_predictor import BranchPredictor

def test_default_prediction():
    """
    Function: test_default_prediction
    Prueba que la predicción por defecto sea "no tomado" para cualquier PC no registrado.
    Example:
        test_default_prediction()
    """
    print("Test: predicción por defecto (no tomado)")
    bp = BranchPredictor()
    pc = 0x100

    result = bp.predict(pc)
    assert result["taken"] is False
    print("Predicción por defecto (not taken) pasó correctamente.")

def test_prediction_update_taken():
    """
    Function: test_prediction_update_taken
    Prueba que la actualización de la predicción a "tomado" funcione correctamente.
    Example:
        test_prediction_update_taken()
    """
    print("🔧 Test: actualización de predicción a tomado")
    bp = BranchPredictor()
    pc = 0x104

    bp.update(pc, True)
    result = bp.predict(pc)
    assert result["taken"] is True
    print("Predicción tomada actualizada correctamente.")

def test_prediction_update_not_taken():
    """
    Function: test_prediction_update_not_taken
    Prueba que la actualización de la predicción a "no tomado" funcione correctamente.
    Example:
        test_prediction_update_not_taken()
    """
    print("🔧 Test: actualización de predicción a no tomado")
    bp = BranchPredictor()
    pc = 0x108

    bp.update(pc, False)
    result = bp.predict(pc)
    assert result["taken"] is False
    print("Predicción no tomada actualizada correctamente.")

def test_flush_required_on_mispredict():
    """
    Function: test_flush_required_on_mispredict
    Prueba la detección de la necesidad de flush cuando hay una predicción errónea.
    Example:
        test_flush_required_on_mispredict()
    """
    print("Test: detección de flush por predicción errónea")
    bp = BranchPredictor()
    pc = 0x10C

    # Predice tomado pero no se toma
    bp.update(pc, True)
    assert bp.flush_required(prediction_taken=True, actual_taken=False) is True

    # Predice no tomado pero sí se toma
    assert bp.flush_required(prediction_taken=False, actual_taken=True) is True

    # Predice correctamente → no flush
    assert bp.flush_required(prediction_taken=True, actual_taken=True) is False
    assert bp.flush_required(prediction_taken=False, actual_taken=False) is False

    print("Flush por predicción incorrecta detectado correctamente.")

if __name__ == "__main__":
    test_default_prediction()
    test_prediction_update_taken()
    test_prediction_update_not_taken()
    test_flush_required_on_mispredict()
