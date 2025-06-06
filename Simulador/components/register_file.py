class RegisterFile:
    # inicializar los registros x0 a x31
    def __init__(self):
        self.registers = {f'x{i}': 0 for i in range(32)}
        self.registers['x0'] = 0  # x0 siempre tiene el valor 0 (hardwired)

    # devuelve el valor actual del registro lanza error si el nombre es invalido
    def read(self, reg_name: str) -> int:
        if reg_name not in self.registers:
            raise ValueError(f"Register {reg_name} does not exist.")
        return self.registers[reg_name]

    # escribe un valor en el registro, si es x0 lo ignora, ademas valida si el registro existe
    def write(self, reg_name: str, value: int):
        if reg_name == 'x0':
            # Ignora escritura en x0
            return
        if reg_name not in self.registers:
            raise ValueError(f"Register {reg_name} does not exist.")
        self.registers[reg_name] = value

    # devuelve una copia de todos los registros
    def dump(self) -> dict:
        # Devuelve una copia de todos los valores de los registros
        return self.registers.copy()

    def reset(self):
        # Reinicia todos los registros a 0, excepto x0
        for key in self.registers:
            if key != 'x0':
                self.registers[key] = 0

    # Representación textual de todos los registros
    def __str__(self):
        lines = [f"{reg}: {val}" for reg, val in self.registers.items()]
        return "\n".join(lines)
