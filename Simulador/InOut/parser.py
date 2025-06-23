from core.instruction import Instruction
import re

class Parser:
    def __init__(self):
        self.instructions = []
        self.labels = {}

    def parse(self, lines: list[str], base_address=0) -> list[Instruction]:
        self.instructions = []
        self.labels = {}

        # Primera pasada: registrar todas las etiquetas con su dirección
        current_address = base_address
        for line in lines:
            clean_line = self._clean_line(line)
            if not clean_line:
                continue
            # Extraer todas las etiquetas al inicio de la línea
            while ':' in clean_line:
                label, rest = clean_line.split(':', 1)
                label = label.strip()
                self.labels[label] = current_address
                clean_line = rest.strip()
            if clean_line:
                current_address += 4

        # Segunda pasada: crear instrucciones y resolver etiquetas
        current_address = base_address
        for line in lines:
            clean_line = self._clean_line(line)
            if not clean_line:
                continue

            # Remover todas las etiquetas al inicio de la línea
            while ':' in clean_line:
                _, rest = clean_line.split(':', 1)
                clean_line = rest.strip()
            if not clean_line:
                continue  # Solo tenía etiqueta(s)

            tokens = self._split_tokens(clean_line)
            if not tokens:
                continue

            # Resolver etiquetas en instrucciones de salto y memoria
            opcode = tokens[0]
            # Instrucciones tipo branch y jump
            if opcode in {"beq", "bne", "blt", "bge", "bltu", "bgeu"}:
                label_or_imm = tokens[-1]
                if not self._is_number(label_or_imm):
                    if label_or_imm in self.labels:
                        offset = self.labels[label_or_imm] - current_address
                        tokens[-1] = str(offset)
                    else:
                        raise ValueError(f"Etiqueta no encontrada: {label_or_imm}")
                clean_line = " ".join(tokens)
            # Instrucción jal con etiqueta
            elif opcode == "jal" and len(tokens) in (2, 3):
                # jal label  o  jal rd, label
                label_idx = 1 if len(tokens) == 2 else 2
                label_or_imm = tokens[label_idx]
                if not self._is_number(label_or_imm):
                    if label_or_imm in self.labels:
                        offset = self.labels[label_or_imm] - current_address
                        tokens[label_idx] = str(offset)
                    else:
                        raise ValueError(f"Etiqueta no encontrada: {label_or_imm}")
                clean_line = " ".join(tokens)
            # Instrucción jalr con etiqueta (poco común, pero soportado)
            elif opcode == "jalr" and len(tokens) == 3:
                # jalr rd, label(rs1)
                mem = tokens[2]
                match = re.match(r"(-?\w+)\((\w+)\)", mem)
                if match:
                    label_or_imm, rs1 = match.groups()
                    if not self._is_number(label_or_imm):
                        if label_or_imm in self.labels:
                            offset = self.labels[label_or_imm] - current_address
                            tokens[2] = f"{offset}({rs1})"
                        else:
                            raise ValueError(f"Etiqueta no encontrada: {label_or_imm}")
                    clean_line = " ".join(tokens)
            # Instrucciones de memoria con etiqueta como offset
            elif opcode in {"lw", "sw"} and len(tokens) == 3:
                mem = tokens[2]
                match = re.match(r"(-?\w+)\((\w+)\)", mem)
                if match:
                    label_or_imm, rs1 = match.groups()
                    if not self._is_number(label_or_imm):
                        if label_or_imm in self.labels:
                            offset = self.labels[label_or_imm] - current_address
                            tokens[2] = f"{offset}({rs1})"
                        else:
                            raise ValueError(f"Etiqueta no encontrada: {label_or_imm}")
                    clean_line = " ".join(tokens)

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
        # Elimina comentarios y espacios
        line = line.split('#')[0]
        return line.strip()

    def _split_tokens(self, line: str) -> list:
        # Divide la línea en tokens, respetando paréntesis y comas
        # Ejemplo: lw x1, 0(x2) -> ['lw', 'x1', '0(x2)']
        tokens = []
        token = ''
        in_paren = False
        for c in line:
            if c == '(':
                in_paren = True
                token += c
            elif c == ')':
                in_paren = False
                token += c
            elif c == ',' and not in_paren:
                if token.strip():
                    tokens.append(token.strip())
                token = ''
            elif c.isspace() and not in_paren:
                if token.strip():
                    tokens.append(token.strip())
                token = ''
            else:
                token += c
        if token.strip():
            tokens.append(token.strip())
        return tokens

    def _is_number(self, s: str) -> bool:
        # Soporta decimales, negativos y hexadecimales
        try:
            int(s, 0)
            return True
        except Exception:
            return False

    def get_labels(self) -> dict:
        return self.labels.copy()
