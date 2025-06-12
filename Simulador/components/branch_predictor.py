class BranchPredictor:
    def __init__(self):
        """
        Inicializa una tabla de predicción con 1-bit por dirección (PC).
        Por defecto, se predice "no tomado".
        """
        self.predictor_table = {}  # key: PC, value: True (taken) / False (not taken)

    def predict(self, pc: int) -> dict:
        """
        Realiza una predicción para una instrucción en PC.

        Retorna:
        - dict con:
            - 'taken': True/False
            - 'target': dirección predicha (si se predice tomado)
        """
        prediction = self.predictor_table.get(pc, False)  # default: not taken
        return {
            "taken": prediction,
            "target": None  # target se debe calcular por fuera si es necesario
        }

    def update(self, pc: int, taken: bool):
        """
        Actualiza la tabla de predicción con el resultado real.

        Params:
        - pc: dirección de la instrucción de salto
        - taken: True si se tomó el salto, False si no
        """
        self.predictor_table[pc] = taken

    def flush_required(self, prediction_taken: bool, actual_taken: bool) -> bool:
        """
        Determina si es necesario hacer un flush debido a una predicción errónea.

        Retorna True si la predicción fue incorrecta.
        """
        return prediction_taken != actual_taken
