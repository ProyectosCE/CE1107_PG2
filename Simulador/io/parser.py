from core.instruction import Instruction

class Parser:
    def __init__(self):
        self.instructions = []  # Lista de objetos Instruction
        self.labels = {}        # Diccionario de etiquetas a direcciones

    def parse(self, lines: list[str], base_address=0) -> list[Instruction]:
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
        Elimina comentarios y espacios de una línea.
        """
        line = line.split('#')[0]
        return line.strip()

    # devuelve el diccionario de etiquetas procesadas
    def get_labels(self) -> dict:
        return self.labels.copy()
