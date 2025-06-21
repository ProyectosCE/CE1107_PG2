import tkinter as tk
from tkinter import ttk


class RiscVSimulatorApp(tk.Tk):
    # Ventana principal del simulador RISC-V.

    def __init__(self):
        super().__init__()
        self.title("Simulador RISC-V")
        self.minsize(width=1000, height=600)

        # Barra de menú
        self._create_menu_bar()

        # Distribución del grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        # Secciones de la UI
        self._create_code_area()
        self._create_simulation_area()
        self._create_status_area()

    # ───────────────────────── MENÚ SUPERIOR ────────────────────────────
    def _create_menu_bar(self):
        menu_bar = tk.Menu(self)

        # Menú «Configuración»
        config_menu = tk.Menu(menu_bar, tearoff=0)
        config_menu.add_command(
            label="Opciones de configuración",
            command=self._open_config_window
        )
        menu_bar.add_cascade(label="Configuración", menu=config_menu)

        self.config(menu=menu_bar)

    def _open_config_window(self):
        """Muestra una ventana emergente (modal) con opciones de configuración."""
        cfg = tk.Toplevel(self)
        cfg.title("Opciones de configuración")
        cfg.geometry("300x200")
        cfg.grab_set()  # Ventana modal

        tk.Label(cfg, text="Configuraciones del simulador",
                 font=("Arial", 12, "bold")).pack(pady=10)

        tk.Checkbutton(cfg, text="Habilitar modo detallado").pack(
            anchor="w", padx=20, pady=5)

        tk.Button(cfg, text="Guardar", command=cfg.destroy).pack(pady=20)

    # ───────────────────────── SECCIÓN CÓDIGO ───────────────────────────
    def _create_code_area(self):
        code_frame = tk.Frame(self)
        code_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        tk.Label(code_frame, text="Código RISC-V",
                 font=("Arial", 12, "bold")).pack(anchor="w")

        self.code_space = tk.Text(code_frame, width=30)
        self.code_space.pack(expand=True, fill="both")

    # ──────────────────────── SECCIÓN SIMULACIÓN ────────────────────────
    def _create_simulation_area(self):
        sim_frame = tk.Frame(self)
        sim_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        tk.Label(sim_frame, text="Simulación",
                 font=("Arial", 14, "bold")).pack(anchor="center", pady=(5, 10))

        notebook = ttk.Notebook(sim_frame)
        notebook.pack(expand=True, fill="both")

        # Pestaña 1
        ciclo_frame = tk.Frame(notebook)
        notebook.add(ciclo_frame, text="Procesador 1")
        tk.Label(ciclo_frame, text="Procesador 1",
                 font=("Arial", 11)).pack(padx=10, pady=10)

        # Pestaña 2
        pipeline_frame = tk.Frame(notebook)
        notebook.add(pipeline_frame, text="Procesador 2")
        tk.Label(pipeline_frame, text="Procesador 2",
                 font=("Arial", 11)).pack(padx=10, pady=10)

    # ───────────────────────── SECCIÓN ESTADO ───────────────────────────
    def _create_status_area(self):
        reg_frame = tk.Frame(self)
        reg_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        tk.Label(reg_frame, text="Estado del Sistema",
                 font=("Arial", 12, "bold")).pack(anchor="w")

        self.ciclo_label = tk.Label(reg_frame, text="Ciclo: 0")
        self.ciclo_label.pack(anchor="w", padx=5)

        self.tiempo_label = tk.Label(reg_frame, text="Tiempo: 0.0 s")
        self.tiempo_label.pack(anchor="w", padx=5)

        self.pc_label = tk.Label(reg_frame, text="PC: 0x00000000")
        self.pc_label.pack(anchor="w", padx=5)

        tk.Label(reg_frame, text="Registros", font=("Arial", 12, "bold")).pack(
            anchor="w", pady=(10, 0))

        self.reg_labels = []
        for i in range(8):
            lbl = tk.Label(reg_frame, text=f"x{i:02d}: 0x00000000", anchor="w")
            lbl.pack(fill="x", padx=5)
            self.reg_labels.append(lbl)
