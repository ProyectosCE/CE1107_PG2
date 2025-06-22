from core.instruction import Instruction

class Metrics:
    def __init__(self, name=""):
        self.name = name
        self.reset()

    def reset(self):
        self.ciclos_totales = 0
        self.instrucciones_retiradas = 0
        self.branches_totales = 0
        self.branches_acertados = 0

    def tick(self):
        """Incrementa el conteo de ciclos."""
        self.ciclos_totales += 1

    def track_writeback(self, instr: Instruction):
        """Se llama cuando una instrucción alcanza WB (retirada)."""
        if instr.opcode != "nop":
            self.instrucciones_retiradas += 1

    def track_branch(self, predicted: bool, actual: bool):
        """Se llama para cada instrucción tipo branch para comparar predicción vs resultado real."""
        self.branches_totales += 1
        if predicted == actual:
            self.branches_acertados += 1

    def display(self, pipeline=None):
        """
        Imprime las métricas recolectadas.
        Si se pasa un pipeline, intenta contar instrucciones en MEM_WB.
        """
        print(f"\n MÉTRICAS DE SIMULACIÓN - {self.name}")
        
        if pipeline:
            self.ciclos_totales = pipeline.get_cycle()

            # Extraer conteo de instrucciones reales ejecutadas
            stages = [pipeline.IF_ID, pipeline.ID_EX, pipeline.EX_MEM, pipeline.MEM_WB]
            self.instrucciones_retiradas = sum(
                1 for stage in stages if stage["instr"].opcode != "nop"
            )

        print(f"  Ciclos totales              : {self.ciclos_totales}")
        print(f"  Instrucciones retiradas     : {self.instrucciones_retiradas}")
        cpi = (self.ciclos_totales / self.instrucciones_retiradas) if self.instrucciones_retiradas else 0
        print(f"  CPI (Ciclos por instrucción): {cpi:.2f}")

        if self.branches_totales > 0:
            accuracy = (self.branches_acertados / self.branches_totales) * 100
            print(f"  Branches totales            : {self.branches_totales}")
            print(f"  Branches acertados          : {self.branches_acertados}")
            print(f"  Precisión del predictor     : {accuracy:.2f}%")
        else:
            print("  No se ejecutaron instrucciones de salto.")
