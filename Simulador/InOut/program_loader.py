import os

class ProgramLoader:
    VALID_EXTENSIONS = {'.s', '.asm'}

    @staticmethod
    def load_program(filepath: str) -> list[str]:
        """
        Carga un programa RISC-V desde un archivo de texto (.s o .asm).
        Elimina comentarios y líneas vacías.

        Params:
            filepath (str): Ruta del archivo

        Returns:
            list[str]: Lista de instrucciones como strings limpias
        """
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")

        _, ext = os.path.splitext(filepath)
        if ext not in ProgramLoader.VALID_EXTENSIONS:
            raise ValueError(f"Extensión inválida: '{ext}'. Se requiere .s o .asm")

        lines = []
        with open(filepath, 'r') as file:
            for raw_line in file:
                clean = ProgramLoader._clean_line(raw_line)
                if clean:
                    lines.append(clean)
        return lines

    @staticmethod
    def _clean_line(line: str) -> str:
        """
        Elimina comentarios y espacios innecesarios de una línea.

        Params:
            line (str): línea del archivo original

        Returns:
            str: línea limpia (vacía si era comentario)
        """
        # Eliminar comentarios tipo # o //
        line = line.split('#')[0]
        line = line.split('//')[0]
        return line.strip()
