import tkinter as tk
from tkinter import ttk, messagebox
# Importación de vistas
from sim_view import ALL_VIEWS


class RiscVSimulatorApp(tk.Tk):
    """Ventana principal del simulador RISC-V."""

    # ────────────────────────────────────────────────────────────────────
    def __init__(self):
        super().__init__()
        self.title("Simulador RISC-V")
        self.minsize(width=1000, height=600)

        self.active_views = [True, True, False, False]
        self._tabs = {}

        self._create_menu_bar()

        # Aquí reemplazamos el grid principal por un PanedWindow horizontal
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill='both', expand=True)

        # Creamos 3 frames para las columnas
        self.code_frame = tk.Frame(self.paned)
        self.sim_frame = tk.Frame(self.paned)
        self.status_frame = tk.Frame(self.paned)

        # Añadimos los frames al paned window
        self.paned.add(self.code_frame, weight=1)
        self.paned.add(self.sim_frame, weight=2)
        self.paned.add(self.status_frame, weight=1)

        # Ahora inicializamos cada sección dentro de su frame
        self._create_code_area()
        self._create_simulation_area()
        self._create_status_area()

    # ───────────────────────── MENÚ SUPERIOR ────────────────────────────
    def _create_menu_bar(self):
        menu_bar = tk.Menu(self)

        config_menu = tk.Menu(menu_bar, tearoff=0)
        config_menu.add_command(
            label="Opciones de configuración",
            command=self._open_config_window
        )
        menu_bar.add_cascade(label="Configuración", menu=config_menu)

        self.config(menu=menu_bar)

    def _open_config_window(self):
        # Ventana modal para escoger exactamente 2 vistas.
        cfg = tk.Toplevel(self)
        cfg.title("Opciones de configuración")
        cfg.geometry("320x260")
        cfg.grab_set()

        tk.Label(cfg,
                 text="Selecciona exactamente 2 vistas:",
                 font=("Arial", 11, "bold")).pack(pady=(10, 5))

        # Variables ligadas al estado actual
        self._opt_vars = [tk.BooleanVar(value=v) for v in self.active_views]

        # Orden histórico de selección (las que ya estaban activas primero)
        self._selection_order = [i for i, v in enumerate(self.active_views) if v]

        textos = ["Vista 1", "Vista 2", "Vista 3", "Vista 4"]
        for idx, (txt, var) in enumerate(zip(textos, self._opt_vars)):
            tk.Checkbutton(cfg,
                           text=txt,
                           variable=var,
                           command=lambda i=idx: self._on_option_toggle(i)
                           ).pack(anchor="w", padx=25, pady=2)

        # Botones
        btns = tk.Frame(cfg)
        btns.pack(pady=15)

        tk.Button(btns, text="Cancelar",
                  width=10, command=cfg.destroy).pack(side="left", padx=5)

        tk.Button(btns, text="Guardar",
                  width=10, command=lambda: self._save_config(cfg)).pack(
            side="right", padx=5)

    def _on_option_toggle(self, idx):
        # Mantiene siempre ≤2 opciones activas.

        var = self._opt_vars[idx]

        if var.get():  # Se acaba de activar
            self._selection_order.append(idx)
            if len(self._selection_order) > 2:
                old_idx = self._selection_order.pop(0)  # la más antigua
                self._opt_vars[old_idx].set(False)
        else:  # Se acaba de desactivar
            if idx in self._selection_order:
                self._selection_order.remove(idx)

    def _save_config(self, window):
        # Guarda selección solo si hay exactamente 2 vistas activas.
        new_selection = [var.get() for var in self._opt_vars]

        if sum(new_selection) != 2:
            messagebox.showerror(
                "Número incorrecto de vistas",
                "Debes tener exactamente 2 vistas activas.")
            return

        self.active_views = new_selection
        self._refresh_sim_views()
        window.destroy()

    # ───────────────────────── SECCIÓN CÓDIGO ───────────────────────────
    def _create_code_area(self):
        tk.Label(self.code_frame, text="Código RISC-V",
                 font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        self.code_space = tk.Text(self.code_frame, width=30)
        self.code_space.pack(expand=True, fill="both", padx=5, pady=5)


    # ──────────────────────── SECCIÓN SIMULACIÓN ────────────────────────
    def _create_simulation_area(self):
        tk.Label(self.sim_frame, text="Simulación",
                 font=("Arial", 14, "bold")).pack(anchor="center", pady=(5, 10))
        self.notebook = ttk.Notebook(self.sim_frame)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)
        self._refresh_sim_views()
    def _refresh_sim_views(self):
        for idx, active in enumerate(self.active_views):
            if active and idx not in self._tabs:
                frame = ALL_VIEWS[idx](self.notebook)
                self.notebook.add(frame, text=f"Vista {idx+1}")
                self._tabs[idx] = frame
            elif not active and idx in self._tabs:
                frame = self._tabs.pop(idx)
                self.notebook.forget(frame)
                frame.destroy()
       #self._tabs[0].highlight("alu") # Ejemplo prueba de resaltado

    # ───────────────────────── SECCIÓN ESTADO ───────────────────────────
    def _create_status_area(self):
        tk.Label(self.status_frame, text="Estado del Sistema",
                 font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        self.ciclo_label = tk.Label(self.status_frame, text="Ciclo: 0")
        self.ciclo_label.pack(anchor="w", padx=5)
        self.tiempo_label = tk.Label(self.status_frame, text="Tiempo: 0.0 s")
        self.tiempo_label.pack(anchor="w", padx=5)
        self.pc_label = tk.Label(self.status_frame, text="PC: 0x00000000")
        self.pc_label.pack(anchor="w", padx=5)
        tk.Label(self.status_frame, text="Registros",
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 0), padx=5)
        self.reg_labels = []
        for i in range(8):
            lbl = tk.Label(self.status_frame, text=f"x{i:02d}: 0x00000000", anchor="w")
            lbl.pack(fill="x", padx=5)
            self.reg_labels.append(lbl)
