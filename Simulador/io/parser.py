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

from core.instruction import Instruction

"""
Class: Parser
Clase encargada de analizar líneas de código ensamblador, identificar etiquetas y construir instrucciones para el simulador.

Attributes:
- instructions: list - lista de objetos Instruction generados tras el parseo.
- labels: dict - diccionario que asocia etiquetas a direcciones de memoria.

Constructor:
- __init__: Inicializa las estructuras para instrucciones y etiquetas.

Methods:
- parse: Procesa una lista de líneas de código, identifica etiquetas y construye instrucciones.
- _clean_line: Elimina comentarios y espacios de una línea.
- get_labels: Devuelve una copia del diccionario de etiquetas procesadas.

Example:
    parser = Parser()
    instrucciones = parser.parse(["start: addi x1, x0, 5", "beq x1, x0, start"])
    print(parser.get_labels())
"""

class Parser:
    def __init__(self):
        """
        Function: __init__
        Inicializa las listas de instrucciones y etiquetas.
        """
        self.instructions = []  # Lista de objetos Instruction
        self.labels = {}        # Diccionario de etiquetas a direcciones

    def parse(self, lines: list[str], base_address=0) -> list[Instruction]:
        """
        Function: parse
        Procesa una lista de líneas de código ensamblador, identifica etiquetas y construye instrucciones.
        Params:
        - lines: list[str] - lista de líneas de código fuente.
        - base_address: int - dirección base para la primera instrucción.
        Returns:
        - list[Instruction]: lista de instrucciones procesadas.
        Example:
            instrucciones = parser.parse(["loop: add x1, x2, x3", "beq x1, x0, loop"])
        """
        self.instructions = []
        self.labels = {}

        # Primera pasada: registrar etiquetas
        current_address = base_address
        for line in lines:
            clean_line = self._clean_line(line)
            if not clean_line:
                continue
            if ":" in clean_line:
                label = clean_line.split(":")[0].strip()
                self.labels[label] = current_address
            else:
                current_address += 4

        # Segunda pasada: construir instrucciones
        current_address = base_address
        for line in lines:
            clean_line = self._clean_line(line)
            if not clean_line:
                continue

            if ":" in clean_line:
                # Línea con etiqueta e instrucción
                label_part, instr_part = clean_line.split(":", 1)
                clean_line = instr_part.strip()
                if not clean_line:
                    continue  # La línea solo tenía una etiqueta
            else:
                # Línea sin etiqueta
                pass  # clean_line ya está listo

            tokens = clean_line.split()

            # Reemplazo de etiquetas si es necesario
            if tokens[0] in {"beq", "bne", "jal"}:
                label_or_imm = tokens[-1]
                try:
                    int(label_or_imm)
                except ValueError:
                    if label_or_imm in self.labels:
                        offset = self.labels[label_or_imm] - current_address
                        tokens[-1] = str(offset)
                        clean_line = " ".join(tokens)
                    else:
                        raise ValueError(f"Etiqueta no encontrada: {label_or_imm}")

            instr = Instruction(clean_line, current_address)
            self.instructions.append(instr)
            current_address += 4

        return self.instructions

    def _clean_line(self, line: str) -> str:
        """
        Function: _clean_line
        Elimina comentarios y espacios de una línea.
        Params:
        - line: str - línea de código fuente.
        Returns:
        - str: línea limpia, sin comentarios ni espacios.
        Example:
            limpia = self._clean_line("addi x1, x0, 5 # comentario")
        """
        line = line.split('#')[0]
        return line.strip()

    def get_labels(self) -> dict:
        """
        Function: get_labels
        Devuelve una copia del diccionario de etiquetas procesadas.
        Returns:
        - dict: copia del diccionario de etiquetas.
        Example:
            etiquetas = parser.get_labels()
        """
        return self.labels.copy()
