from core.instruction import Instruction

class Parser:
    def __init__(self):
        self.instructions = []
        self.labels = {}

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

        # Segunda pasada: crear instrucciones y resolver etiquetas
        current_address = base_address
        for line in lines:
            clean_line = self._clean_line(line)
            if not clean_line:
                continue

            if ":" in clean_line:
                _, instr_part = clean_line.split(":", 1)
                clean_line = instr_part.strip()
                if not clean_line:
                    continue  # Solo tenía etiqueta

            tokens = clean_line.split()

            # Resolver etiquetas (branch/jump)
            if tokens[0] in {"beq", "bne", "jal"}:
                label_or_imm = tokens[-1]
                try:
                    int(label_or_imm)  # Ya es un inmediato
                except ValueError:
                    if label_or_imm in self.labels:
                        offset = self.labels[label_or_imm] - current_address
                        tokens[-1] = str(offset)
                        clean_line = " ".join(tokens)
                    else:
                        raise ValueError(f"Etiqueta no encontrada: {label_or_imm}")

            # Crear instrucción y validar
            try:
                instr = Instruction(clean_line, current_address)
                if not instr.is_valid():
                    raise ValueError(f"Instrucción inválida: '{clean_line}' en PC={current_address}")
                self.instructions.append(instr)
                current_address += 4
            except Exception as e:
                raise ValueError(f"Error al parsear instrucción en PC={current_address}: {e}")

        return self.instructions

    def _clean_line(self, line: str) -> str:
        line = line.split('#')[0]
        return line.strip()

    def get_labels(self) -> dict:
        return self.labels.copy()
