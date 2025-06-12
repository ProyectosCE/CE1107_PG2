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
Class: BranchPredictor
Clase que implementa un predictor de saltos simple de 1 bit por dirección (PC), para mejorar el flujo de instrucciones en el pipeline.

Attributes:
- predictor_table: dict - tabla que asocia cada PC con un bit de predicción (True: tomado, False: no tomado).

Constructor:
- __init__: Inicializa la tabla de predicción.

Methods:
- predict: Realiza una predicción para una instrucción dada su dirección.
- update: Actualiza la tabla de predicción con el resultado real del salto.
- flush_required: Determina si es necesario hacer un flush por predicción errónea.

Example:
    predictor = BranchPredictor()
    pred = predictor.predict(8)
    predictor.update(8, True)
    if predictor.flush_required(pred["taken"], True):
        # hacer flush
"""

class BranchPredictor:
    def __init__(self):
        """
        Function: __init__
        Inicializa una tabla de predicción con 1-bit por dirección (PC).
        Por defecto, se predice "no tomado".
        """
        self.predictor_table = {}  # key: PC, value: True (taken) / False (not taken)

    def predict(self, pc: int) -> dict:
        """
        Function: predict
        Realiza una predicción para una instrucción en PC.
        Params:
        - pc: int - dirección de la instrucción de salto.
        Returns:
        - dict: contiene 'taken' (bool) y 'target' (None, el target se calcula externamente).
        Example:
            pred = predictor.predict(12)
        """
        prediction = self.predictor_table.get(pc, False)  # default: not taken
        return {
            "taken": prediction,
            "target": None  # target se debe calcular por fuera si es necesario
        }

    def update(self, pc: int, taken: bool):
        """
        Function: update
        Actualiza la tabla de predicción con el resultado real del salto.
        Params:
        - pc: int - dirección de la instrucción de salto.
        - taken: bool - True si se tomó el salto, False si no.
        Example:
            predictor.update(12, True)
        """
        self.predictor_table[pc] = taken

    def flush_required(self, prediction_taken: bool, actual_taken: bool) -> bool:
        """
        Function: flush_required
        Determina si es necesario hacer un flush debido a una predicción errónea.
        Params:
        - prediction_taken: bool - valor predicho.
        - actual_taken: bool - valor real.
        Returns:
        - bool: True si la predicción fue incorrecta.
        Example:
            if predictor.flush_required(pred["taken"], True):
                # hacer flush
        """
        return prediction_taken != actual_taken
