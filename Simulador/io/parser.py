from core.instruction import Instruction

class Parser:
    def __init__(self):
        self.instructions = []  # Lista de objetos Instruction
        self.labels = {}        # Diccionario de etiquetas a direcciones

    def parse(self, lines: list[str], base_address=0) -> list[Instruction]:
        """
        Parsea una lista de líneas en RISC-V assembly.
        Devuelve una lista de instrucciones con sus direcciones.
        """
        self.instructions = []
        self.labels = {}

        # Primera pasada: detectar etiquetas y guarda dirección asociada
        # aun no crea instrucciones todavía
        current_address = base_address
        for line in lines:
            clean_line = self._clean_line(line)
            if not clean_line:
                continue
            if ":" in clean_line:
                label = clean_line.replace(":", "").strip()
                self.labels[label] = current_address
            else:
                current_address += 4

        # Segunda pasada: procesar instrucciones válidas
        # sustituye etiquetdas por desplazamientos relativos si son saltos
        current_address = base_address
        for line in lines:
            clean_line = self._clean_line(line)
            if not clean_line or ":" in clean_line:
                continue
            # Reemplazar etiquetas en ramas o saltos
            tokens = clean_line.split()
            if tokens[0] in {"beq", "bne", "jal"} and tokens[-1] in self.labels:
                label = tokens[-1]
                offset = self.labels[label] - current_address
                clean_line = " ".join(tokens[:-1] + [str(offset)])

            instr = Instruction(clean_line, current_address)
            self.instructions.append(instr)
            current_address += 4

        return self.instructions

    def _clean_line(self, line: str) -> str:
        """
        Elimina comentarios y espacios de una línea.
        """
        line = line.split('#')[0]
        return line.strip()

    # devuelve el diccionario de etiquetas procesadas
    def get_labels(self) -> dict:
        return self.labels.copy()
