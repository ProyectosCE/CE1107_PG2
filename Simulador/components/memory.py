class Memory:
    def __init__(self, size_in_words=1024):
        """
        Inicializa una memoria RAM de 1024 palabras (4096 bytes).
        size_in_words: cantidad de celdas de 32 bits.
        """
        self.size = size_in_words
        self.data = [0] * self.size

    # Valida que la dirección sea múltiplo de 4 y esté dentro del rango de memoria.
    def _check_address(self, address: int):
        if address % 4 != 0:
            raise ValueError(f"Dirección no alineada a 4 bytes: {address}")
        index = address // 4
        if index < 0 or index >= self.size:
            raise ValueError(f"Dirección fuera de rango: {address}")
        return index

    # Devuelve el valor de una word en la dirección dada, requiera dirección válida.
    def load_word(self, address: int) -> int:
        """Lee una palabra de 32 bits desde la dirección dada."""
        index = self._check_address(address)
        return self.data[index]

    # escribe un valor de 32 bits en memoria, evita escrituras fuera de rango o desalineadas.
    def store_word(self, address: int, value: int):
        """Escribe una palabra de 32 bits en la dirección dada."""
        index = self._check_address(address)
        self.data[index] = value

    # Permite cargar un programa o bloque de datos a partir de una dirección inicial, cada valor se guarda como una word de 4 bytes.
    def load_program(self, values: list, start_address: int = 0):
        """
        Carga una lista de valores enteros en memoria comenzando desde start_address.
        Se usa para cargar instrucciones compiladas o datos de entrada.
        """
        for offset, val in enumerate(values):
            addr = start_address + offset * 4
            self.store_word(addr, val)

    # Devuelve un diccionario con el contenido de memoria
    def dump(self, from_addr=0, to_addr=None) -> dict:
        """
        Devuelve una representación de memoria entre dos direcciones (inclusive).
        Ideal para mostrar en GUI o logs.
        """
        if to_addr is None:
            to_addr = (self.size - 1) * 4
        output = {}
        for addr in range(from_addr, to_addr + 1, 4):
            output[addr] = self.load_word(addr)
        return output

    # Limpia la memoria
    def reset(self):
        """Limpia toda la memoria."""
        self.data = [0] * self.size
