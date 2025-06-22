import tkinter as tk
from tkinter import ttk, messagebox
# Importación de vistas
from sim_view import ALL_VIEWS
from view_status import ViewStatus


class RiscVSimulatorApp(tk.Tk):
    """Ventana principal del simulador RISC-V."""

    def __init__(self):
        super().__init__()
        self.title("Simulador RISC-V")
        self.minsize(width=1500, height=600)

        self.active_views = [True, True, False, False]
        self._tabs = {}

        self._create_menu_bar()
        self._create_toolbar()

        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill='both', expand=True)

        self.code_frame = tk.Frame(self.paned, bd=1, relief="solid")
        self.sim_frame = tk.Frame(self.paned, bd=1, relief="solid")
        self.status_frame1 = tk.Frame(self.paned, width=180, bd=1, relief="solid")
        self.status_frame1.pack_propagate(False)
        self.status_frame2 = tk.Frame(self.paned, width=180, bd=1, relief="solid")
        self.status_frame2.pack_propagate(False)

        self.paned.add(self.code_frame, weight=1)
        self.paned.add(self.sim_frame, weight=2)
        self.paned.add(self.status_frame1, weight=1)
        self.paned.add(self.status_frame2, weight=1)

        self._create_code_area()
        self._create_simulation_area()

        # Instancia los dos ViewStatus, uno para cada "estado" de vista activa
        self.view_status_1 = ViewStatus(self.status_frame1, view_name="Sim 1")
        self.view_status_1.pack(fill="both", expand=True)

        self.view_status_2 = ViewStatus(self.status_frame2, view_name="Sim 2")
        self.view_status_2.pack(fill="both", expand=True)

        self._refresh_sim_views()

    """
    ======================================================================
                             Menú de configuración
    ======================================================================
    """


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

        textos = ["Sim 1", "Sim 2", "Sim 3", "Sim 4"]
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
                "Debes tener exactamente 2 Sim activas.")
            return

        self.active_views = new_selection
        self._refresh_sim_views()
        window.destroy()

    """
    ======================================================================
                     Toolbar de control de ejecucion
    ======================================================================
    """
    def _create_toolbar(self):
        bar = tk.Frame(self, bd=1, relief="raised", pady=2)
        bar.pack(fill="x")

        #  a) Paso a paso
        tk.Button(bar, text="←", width=3, command=self._step_backward).pack(side="left", padx=2)
        tk.Button(bar, text="→", width=3, command=self._step_forward).pack(side="left")
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=4)

        # b) Ejecución rítmica
        tk.Label(bar, text="Intervalo (ms):").pack(side="left")
        self.interval_spin = tk.Spinbox(
            bar, from_=1, to=10000, width=5, validate="all",
            validatecommand=(self.register(lambda v: v.isdigit() and int(v) >= 1), "%P")
        )
        self.interval_spin.pack(side="left", padx=2)
        tk.Button(bar, text="Start", command=self._start_timed_exec).pack(side="left")
        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=4)

        # c) Ejecución completa
        tk.Button(bar, text="Run-All", command=self._run_full_exec).pack(side="left", padx=2)

        # d) Detener ejecución continua
        tk.Button(bar, text="Stop", command=self._stop_timed_exec).pack(side="left", padx=2)

        # e) Reset
        tk.Button(bar, text="Reset", command=self._reset_simulation).pack(side="left", padx=2)
    # Callbacks
    def _step_backward(self):
        # Falta para implementar el paso atrás
        print("Step backward un ciclo")

    def _step_forward(self):
        print("Step forward un ciclo")

    def _start_timed_exec(self):
        ms = int(self.interval_spin.get())
        print(f"Ejecución continua: un ciclo cada {ms} ms")

    def _run_full_exec(self):
        print("Ejecutar hasta el final")

    def _stop_timed_exec(self):
        print("Detener ejecución continua")

    def _reset_simulation(self):
        """Reinicia la simulación, limpiando el código y el estado de las vistas."""
        print("Reiniciar simulación")

    """
    ======================================================================
                             Seccion de código
    ======================================================================
    """
    def _create_code_area(self):
        tk.Label(self.code_frame, text="Código RISC-V", font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=5)
        self.code_space = tk.Text(self.code_frame, width=30)
        self.code_space.pack(expand=True, fill="both", padx=5, pady=5)


    """
    ======================================================================
                             Menú de simulacion
    ======================================================================
    """
    def _create_simulation_area(self):
        tk.Label(self.sim_frame, text="Simulación", font=("Arial", 14, "bold")).pack(anchor="center", pady=(5, 10))
        self.notebook = ttk.Notebook(self.sim_frame)
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)

    def _refresh_sim_views(self):
        # Limpia las pestañas
        for idx in list(self._tabs.keys()):
            frame = self._tabs.pop(idx)
            self.notebook.forget(frame)
            frame.destroy()

        # Añade vistas activas en notebook
        for idx, active in enumerate(self.active_views):
            if active:
                frame = ALL_VIEWS[idx](self.notebook)
                self.notebook.add(frame, text=f"Sim {idx + 1}")
                self._tabs[idx] = frame

        vistas_activas = [i for i, v in enumerate(self.active_views) if v]

        if len(vistas_activas) >= 1:
            self.view_status_1.set_view_name(f"Sim {vistas_activas[0] + 1}")
            # Actualiza el estado inicial de la vista 1
            self.view_status_1.update_status(0, 0.0, 0, [0] * 8, {i: 0 for i in range(8)})
            if not self.view_status_1.winfo_ismapped():
                self.view_status_1.pack(fill="both", expand=True)
        else:
            if self.view_status_1.winfo_ismapped():
                self.view_status_1.pack_forget()

        if len(vistas_activas) == 2:
            self.view_status_2.set_view_name(f"Sim {vistas_activas[1] + 1}")
            # Actualiza el estado inicial de la vista 2
            self.view_status_2.update_status(0, 0.0, 0, [0] * 8, {i: 0 for i in range(8)})

            if not self.view_status_2.winfo_ismapped():
                self.view_status_2.pack(fill="both", expand=True)
        else:
            if self.view_status_2.winfo_ismapped():
                self.view_status_2.pack_forget()