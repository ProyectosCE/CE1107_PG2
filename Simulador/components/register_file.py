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
Class: RegisterFile
Clase que simula el banco de registros de un procesador RISC-V, con registros x0 a x31.
Permite leer, escribir, reiniciar y obtener el estado de todos los registros.

Attributes:
- registers: dict - diccionario que almacena los valores de los registros (x0 a x31).

Constructor:
- __init__: Inicializa todos los registros en 0, asegurando que x0 siempre sea 0.

Methods:
- read: Devuelve el valor actual de un registro dado su nombre.
- write: Escribe un valor en un registro, ignorando x0.
- dump: Devuelve una copia del estado de todos los registros.
- reset: Reinicia todos los registros a 0, excepto x0.
- __str__: Devuelve una representación textual de todos los registros.

Example:
    rf = RegisterFile()
    rf.write('x1', 10)
    print(rf.read('x1'))  # Imprime: 10
    print(rf)  # Muestra todos los registros
    rf.reset()
"""

class RegisterFile:
    def __init__(self):
        """
        Function: __init__
        Inicializa los registros x0 a x31 en 0. El registro x0 siempre permanece en 0.
        """
        self.registers = {f'x{i}': 0 for i in range(32)}  # Crea los registros x0-x31
        self.registers['x0'] = 0  # x0 siempre tiene el valor 0 (hardwired)

    def read(self, reg_name: str) -> int:
        """
        Function: read
        Devuelve el valor actual del registro especificado.
        Params:
        - reg_name: str - nombre del registro a leer (ejemplo: 'x5').
        Returns:
        - int: valor almacenado en el registro.
        Restriction:
        Lanza ValueError si el nombre del registro es inválido.
        Example:
            valor = rf.read('x2')
        """
        if reg_name not in self.registers:
            raise ValueError(f"Register {reg_name} does not exist.")
        return self.registers[reg_name]

    def write(self, reg_name: str, value: int):
        """
        Function: write
        Escribe un valor en el registro especificado, ignorando x0.
        Params:
        - reg_name: str - nombre del registro a escribir.
        - value: int - valor a almacenar en el registro.
        Restriction:
        No permite modificar el registro x0. Lanza ValueError si el registro no existe.
        Example:
            rf.write('x3', 42)
        """
        if reg_name == 'x0':
            # Ignora escritura en x0
            return
        if reg_name not in self.registers:
            raise ValueError(f"Register {reg_name} does not exist.")
        self.registers[reg_name] = value

    def dump(self) -> dict:
        """
        Function: dump
        Devuelve una copia del estado de todos los registros.
        Returns:
        - dict: copia del diccionario de registros.
        Example:
            estado = rf.dump()
        """
        return self.registers.copy()

    def reset(self):
        """
        Function: reset
        Reinicia todos los registros a 0, excepto x0.
        Example:
            rf.reset()
        """
        for key in self.registers:
            if key != 'x0':
                self.registers[key] = 0

    def __str__(self):
        """
        Function: __str__
        Devuelve una representación textual de todos los registros.
        Returns:
        - str: texto con los nombres y valores de los registros.
        Example:
            print(rf)
        """
        lines = [f"{reg}: {val}" for reg, val in self.registers.items()]
        return "\n".join(lines)
