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
Class: Memory
Clase que simula una memoria RAM de palabras de 32 bits para el simulador.
Permite almacenar, recuperar y manipular datos enteros en posiciones de memoria alineadas a 4 bytes.

Attributes:
- size: int - cantidad de palabras de 32 bits que puede almacenar la memoria.
- data: list - lista de enteros que representa el contenido de la memoria.

Constructor:
- __init__: Inicializa la memoria con un tamaño dado en palabras de 32 bits.

Methods:
- _check_address: Valida que una dirección sea múltiplo de 4 y esté dentro del rango de memoria.
- load_word: Lee una palabra de 32 bits desde una dirección dada.
- store_word: Escribe una palabra de 32 bits en una dirección dada.
- load_program: Carga una lista de valores en memoria a partir de una dirección inicial.
- dump: Devuelve un diccionario con el contenido de memoria entre dos direcciones.
- reset: Limpia toda la memoria, restaurando su estado inicial.

Example:
    mem = Memory(1024)
    mem.store_word(0, 123)
    print(mem.load_word(0))  # Imprime: 123
    mem.reset()
"""

class Memory:
    def __init__(self, size_in_words=1024):
        """
        Function: __init__
        Inicializa una memoria RAM de 1024 palabras (4096 bytes) por defecto.
        Params:
        - size_in_words: int - cantidad de celdas de 32 bits.
        """
        self.size = size_in_words  # Número de palabras de 32 bits
        self.data = [0] * self.size  # Inicializa la memoria en cero

    def _check_address(self, address: int):
        """
        Function: _check_address
        Valida que la dirección sea múltiplo de 4 y esté dentro del rango de memoria.
        Params:
        - address: int - dirección de memoria a validar.
        Returns:
        - int: índice correspondiente en la lista interna de datos.
        Restriction:
        La dirección debe estar alineada a 4 bytes y dentro del rango de memoria.
        """
        if address % 4 != 0:
            raise ValueError(f"Dirección no alineada a 4 bytes: {address}")
        index = address // 4
        if index < 0 or index >= self.size:
            raise ValueError(f"Dirección fuera de rango: {address}")
        return index

    def load_word(self, address: int) -> int:
        """
        Function: load_word
        Lee una palabra de 32 bits desde la dirección dada.
        Params:
        - address: int - dirección de memoria desde la cual leer.
        Returns:
        - int: valor almacenado en la dirección dada.
        Restriction:
        La dirección debe ser válida y estar alineada a 4 bytes.
        Example:
            valor = mem.load_word(8)
        """
        index = self._check_address(address)  # Validación de dirección
        return self.data[index]

    def store_word(self, address: int, value: int):
        """
        Function: store_word
        Escribe una palabra de 32 bits en la dirección dada.
        Params:
        - address: int - dirección de memoria donde escribir.
        - value: int - valor de 32 bits a almacenar.
        Restriction:
        La dirección debe ser válida y estar alineada a 4 bytes.
        Example:
            mem.store_word(12, 42)
        """
        index = self._check_address(address)  # Validación de dirección
        self.data[index] = value

    def load_program(self, values: list, start_address: int = 0):
        """
        Function: load_program
        Carga una lista de valores enteros en memoria comenzando desde start_address.
        Se usa para cargar instrucciones compiladas o datos de entrada.
        Params:
        - values: list - lista de enteros a cargar en memoria.
        - start_address: int - dirección inicial donde comenzar a cargar los valores.
        Example:
            mem.load_program([1,2,3], 0)
        """
        for offset, val in enumerate(values):
            addr = start_address + offset * 4  # Calcula la dirección alineada
            self.store_word(addr, val)

    def dump(self, from_addr=0, to_addr=None) -> dict:
        """
        Function: dump
        Devuelve una representación de memoria entre dos direcciones (inclusive).
        Ideal para mostrar en GUI o logs.
        Params:
        - from_addr: int - dirección inicial.
        - to_addr: int o None - dirección final (inclusive). Si es None, se usa el final de la memoria.
        Returns:
        - dict: diccionario con direcciones como llaves y valores almacenados.
        Example:
            mem.dump(0, 16)
        """
        if to_addr is None:
            to_addr = (self.size - 1) * 4
        output = {}
        for addr in range(from_addr, to_addr + 1, 4):
            output[addr] = self.load_word(addr)
        return output

    def reset(self):
        """
        Function: reset
        Limpia toda la memoria, restaurando su estado inicial.
        Example:
            mem.reset()
        """
        self.data = [0] * self.size  # Reinicia todos los valores a cero
