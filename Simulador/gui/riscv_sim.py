import tkinter as tk
from tkinter import ttk, messagebox
# Importación de vistas
from .sim_view import ALL_VIEWS
from .view_status import ViewStatus
from collections import deque

from InOut.parser import Parser
from core.simulator_manager import SimulatorManager
from InOut.execution_history import ExecutionHistory


class RiscVSimulatorApp(tk.Tk):
    """Ventana principal del simulador RISC-V."""

    def __init__(self):
        super().__init__()
        self.title("Simulador RISC-V")

        try:
            self.state("zoomed")
        except tk.TclError:
            self.attributes("-zoomed", True)


        self.minsize(width=1500, height=600)

        self.active_views = [True, True, False, False]
        self.active_indices = [0, 1]  # Por defecto, los dos primeros
        self._tabs = {}

        self._sim_names = [
            "Sim 1 (sin unidad de riesgos)",
            "Sim 2 (con unidad de riesgos )",
            "Sim 3 (con predicción de saltos)",
            "Sim 4 (con unidad de riesgos con predicción de saltos)"
        ]

        self._create_menu_bar()
        self._create_toolbar()

        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill='both', expand=True)

        self.code_frame = tk.Frame(self.paned, bd=1, relief="solid")
        self.sim_frame = tk.Frame(self.paned, bd=1, relief="solid")
        self.status_frame1 = tk.Frame(self.paned, width=250, bd=1, relief="solid")
        self.status_frame1.pack_propagate(False)
        self.status_frame2 = tk.Frame(self.paned, width=250, bd=1, relief="solid")
        self.status_frame2.pack_propagate(False)

        # Añade los frames (sin minsize)
        self.paned.add(self.code_frame, weight=1)
        self.paned.add(self.sim_frame, weight=4)
        self.paned.add(self.status_frame1, weight=0)
        self.paned.add(self.status_frame2, weight=0)


        self._create_code_area()
        self._create_simulation_area()

        # Instancia los dos ViewStatus, uno para cada "estado" de vista activa
        self.view_status_1 = ViewStatus(self.status_frame1, view_name="Sim 1")
        self.view_status_1.pack(fill="both", expand=True)

        self.view_status_2 = ViewStatus(self.status_frame2, view_name="Sim 2")
        self.view_status_2.pack(fill="both", expand=True)

        self._refresh_sim_views()

        self._history = {1: deque(maxlen=10), 2: deque(maxlen=10)}  # últimas 10 por sim
        self._history_win = None

        # Inicialización de atributos para el paso a paso
        self._step_manager = None
        self._step_initialized = False
        self._step_program_lines = None

        # Control de ejecución rítmica
        self._timed_exec_running = False
        self._timed_exec_after_id = None
        self._timed_exec_manager = None
        self._timed_exec_program_lines = None
        self._timed_exec_delay = None

    # PRUEBA DE HISTORIAL - Borrar despues
        #self.update_history(1, 1, 0, 0, 0, 0, 0)
        #self.update_history(2, 0, 0, 0, 0, 0, 0)

    """
    ======================================================================
                                API de simulación
    ======================================================================
    """

    def _step_backward(self):
        # Falta para implementar el paso atrás
        print("Step backward un ciclo")

    def _step_forward(self):
        code = self.code_space.get("1.0", tk.END)
        raw_lines = [line for line in code.splitlines() if line.strip()]
        parser = Parser()
        try:
            instructions = parser.parse(raw_lines)
            program_lines = []
            for instr in instructions:
                if hasattr(instr, "raw_line"):
                    program_lines.append(instr.raw_line)
                elif hasattr(instr, "text"):
                    program_lines.append(instr.text)
                else:
                    program_lines.append(instr.opcode + " " + " ".join(str(x) for x in instr.operands))
            if not program_lines or any(not instr.is_valid() for instr in instructions):
                print("Error: El parser generó instrucciones inválidas o vacías.")
                return
        except Exception as e:
            print(f"Error al parsear el código: {e}")
            return

        if not self._step_initialized or self._step_program_lines != program_lines or self._step_manager is None:
            try:
                self._step_manager = SimulatorManager(program_lines, active_indices=self.active_indices)
                for cpu in self._step_manager.cpus:
                    cpu.load_program(program_lines)
                self._step_program_lines = program_lines
                self._step_initialized = True
            except Exception as e:
                print(f"Error al inicializar el simulador: {e}")
                return

        all_finished = True
        for view_idx, sim_idx in enumerate(self.active_indices):
            cpu_name = self._step_manager.cpu_names[sim_idx]
            cpu = self._step_manager.cpus[view_idx]
            try:
                finished = cpu.run_one_cycle()
                metrics = cpu.metrics

                ciclos = metrics.ciclos_totales
                inst = metrics.instrucciones_retiradas
                cpi = metrics.ciclos_totales / metrics.instrucciones_retiradas if metrics.instrucciones_retiradas else 0
                branch_total = metrics.branches_totales
                branch_acertados = metrics.branches_acertados

                # Obtener tiempo real de ejecución
                if hasattr(metrics, "get_elapsed_time"):
                    tiempo = metrics.get_elapsed_time()
                elif hasattr(metrics, "elapsed_time"):
                    tiempo = metrics.elapsed_time
                else:
                    tiempo = 0.0

                # Obtener PC actual del pipeline (preferentemente IF_ID)
                pc = 0
                if hasattr(cpu, "pipeline") and hasattr(cpu.pipeline, "IF_ID"):
                    if hasattr(cpu.pipeline.IF_ID, "pc"):
                        pc = cpu.pipeline.IF_ID.pc
                    elif isinstance(cpu.pipeline.IF_ID, dict) and "pc" in cpu.pipeline.IF_ID:
                        pc = cpu.pipeline.IF_ID["pc"]
                elif hasattr(cpu, "pc"):
                    pc = cpu.pc

                # Si el procesador no tiene atributo pc, intenta obtenerlo del pipeline IF_ID
                if not pc and hasattr(cpu, "pipeline") and hasattr(cpu.pipeline, "IF_ID"):
                    pc = getattr(cpu.pipeline.IF_ID, "pc", 0)
                print(f"\n--- Métricas para {cpu_name} ---")
                print(f"Ciclos totales: {ciclos}")
                print(f"Instrucciones retiradas: {inst}")
                print(f"CPI: {cpi:.2f}")
                print(f"Branches totales: {branch_total}")
                print(f"Branches acertados: {branch_acertados}")
                if metrics.branches_totales:
                    precision = (metrics.branches_acertados / metrics.branches_totales) * 100
                else:
                    precision = 0.0
                print(f"Precisión del predictor: {precision:.2f}%")

                self.update_metrics_sim(view_idx+1, ciclos, inst, cpi, branch_total, branch_acertados, precision)
                self.update_system_state_sim(view_idx+1, ciclos, tiempo, pc)

                # --- Actualizar registros en tiempo real ---
                if hasattr(cpu, "registers") and hasattr(cpu.registers, "dump"):
                    reg_dict = cpu.registers.dump()
                    self.update_registers_sim(view_idx+1, reg_dict)
                else:
                    self.update_registers_sim(view_idx+1, {f"x{i}": 0 for i in range(32)})

                # --- Actualizar memoria en tiempo real ---
                if hasattr(cpu, "data_mem") and hasattr(cpu.data_mem, "dump"):
                    mem_dict = cpu.data_mem.dump()
                    self.update_memory_sim(view_idx+1, mem_dict)
                else:
                    self.update_memory_sim(view_idx+1, {addr: 0 for addr in range(0, 4096, 4)})

                # Si terminó, reiniciar para el próximo step
                if finished:
                    print(f"{cpu_name} ha finalizado la ejecución.")
                else:
                    all_finished = False
            except Exception as e:
                print(f"Error al ejecutar {cpu_name}: {e}")
                all_finished = False

        # --- Guardar historial solo si TODOS han terminado ---
        if all_finished:
            history = ExecutionHistory()
            for view_idx, sim_idx in enumerate(self.active_indices):
                cpu_name = self._step_manager.cpu_names[sim_idx]
                cpu = self._step_manager.cpus[view_idx]
                config = self._step_manager.cpu_configs[sim_idx]
                metrics = cpu.metrics
                history.add_execution(
                    processor_name=cpu_name,
                    metrics=metrics,
                    config=config
                )
            self._step_initialized = False

    def _start_timed_exec(self):
        # Si ya está corriendo la ejecución rítmica, no hacer nada
        if self._timed_exec_running:
            return

        ms = int(self.interval_spin.get())
        print(f"Ejecución rítmica: un ciclo cada {ms} ms")
        code = self.code_space.get("1.0", tk.END)
        raw_lines = [line for line in code.splitlines() if line.strip()]
        parser = Parser()
        try:
            instructions = parser.parse(raw_lines)
            program_lines = []
            for instr in instructions:
                if hasattr(instr, "raw_line"):
                    program_lines.append(instr.raw_line)
                elif hasattr(instr, "text"):
                    program_lines.append(instr.text)
                else:
                    program_lines.append(instr.opcode + " " + " ".join(str(x) for x in instr.operands))
            if not program_lines or any(not instr.is_valid() for instr in instructions):
                print("Error: El parser generó instrucciones inválidas o vacías.")
                return
        except Exception as e:
            print(f"Error al parsear el código: {e}")
            return

        try:
            self._timed_exec_manager = SimulatorManager(program_lines, active_indices=self.active_indices)
            for cpu in self._timed_exec_manager.cpus:
                cpu.load_program(program_lines)
            self._timed_exec_program_lines = program_lines
        except Exception as e:
            print(f"Error al inicializar el simulador: {e}")
            return

        self._timed_exec_running = True
        self._timed_exec_delay = ms
        self._timed_exec_step()  # inicia la ejecución rítmica

    def _timed_exec_step(self):
        if not self._timed_exec_running:
            return

        finished_all = True
        for view_idx, sim_idx in enumerate(self.active_indices):
            cpu_name = self._timed_exec_manager.cpu_names[sim_idx]
            cpu = self._timed_exec_manager.cpus[view_idx]
            try:
                finished = cpu.run_one_cycle()
                metrics = cpu.metrics

                ciclos = metrics.ciclos_totales
                inst = metrics.instrucciones_retiradas
                cpi = metrics.ciclos_totales / metrics.instrucciones_retiradas if metrics.instrucciones_retiradas else 0
                branch_total = metrics.branches_totales
                branch_acertados = metrics.branches_acertados

                if hasattr(metrics, "get_elapsed_time"):
                    tiempo = metrics.get_elapsed_time()
                elif hasattr(metrics, "elapsed_time"):
                    tiempo = metrics.elapsed_time
                else:
                    tiempo = 0.0

                pc = 0
                if hasattr(cpu, "pipeline") and hasattr(cpu.pipeline, "IF_ID"):
                    if hasattr(cpu.pipeline.IF_ID, "pc"):
                        pc = cpu.pipeline.IF_ID.pc
                    elif isinstance(cpu.pipeline.IF_ID, dict) and "pc" in cpu.pipeline.IF_ID:
                        pc = cpu.pipeline.IF_ID["pc"]
                elif hasattr(cpu, "pc"):
                    pc = cpu.pc

                if metrics.branches_totales:
                    precision = (metrics.branches_acertados / metrics.branches_totales) * 100
                else:
                    precision = 0.0

                self.update_metrics_sim(view_idx+1, ciclos, inst, cpi, branch_total, branch_acertados, precision)
                self.update_system_state_sim(view_idx+1, ciclos, tiempo, pc)

                # --- Actualizar registros en tiempo real ---
                if hasattr(cpu, "registers") and hasattr(cpu.registers, "dump"):
                    reg_dict = cpu.registers.dump()
                    self.update_registers_sim(view_idx+1, reg_dict)
                else:
                    self.update_registers_sim(view_idx+1, {f"x{i}": 0 for i in range(32)})

                # --- Actualizar memoria en tiempo real ---
                if hasattr(cpu, "data_mem") and hasattr(cpu.data_mem, "dump"):
                    mem_dict = cpu.data_mem.dump()
                    self.update_memory_sim(view_idx+1, mem_dict)
                else:
                    self.update_memory_sim(view_idx+1, {addr: 0 for addr in range(0, 4096, 4)})

                if not finished:
                    finished_all = False

            except Exception as e:
                print(f"Error al ejecutar {cpu_name}: {e}")
                finished_all = False

        if not finished_all:
            # Programar el siguiente ciclo
            self._timed_exec_after_id = self.after(self._timed_exec_delay, self._timed_exec_step)
        else:
            self._timed_exec_running = False
            self._timed_exec_after_id = None
            print("Ejecución rítmica finalizada.")

            # --- Guardar historial solo si TODOS han terminado ---
            history = ExecutionHistory()
            for view_idx, sim_idx in enumerate(self.active_indices):
                cpu_name = self._timed_exec_manager.cpu_names[sim_idx]
                cpu = self._timed_exec_manager.cpus[view_idx]
                config = self._timed_exec_manager.cpu_configs[sim_idx]
                metrics = cpu.metrics
                history.add_execution(
                    processor_name=cpu_name,
                    metrics=metrics,
                    config=config
                )

    def _stop_timed_exec(self):
        print("Detener ejecución continua")
        # Solo afecta si está corriendo la ejecución rítmica (delay)
        if self._timed_exec_running and self._timed_exec_after_id is not None:
            self.after_cancel(self._timed_exec_after_id)
            self._timed_exec_after_id = None
        self._timed_exec_running = False

    def _run_full_exec(self):
        code = self.code_space.get("1.0", tk.END)
        raw_lines = [line for line in code.splitlines() if line.strip()]
        parser = Parser()
        try:
            instructions = parser.parse(raw_lines)
            program_lines = []
            for instr in instructions:
                if hasattr(instr, "raw_line"):
                    program_lines.append(instr.raw_line)
                elif hasattr(instr, "text"):
                    program_lines.append(instr.text)
                else:
                    program_lines.append(instr.opcode + " " + " ".join(str(x) for x in instr.operands))
            if not program_lines or any(not instr.is_valid() for instr in instructions):
                print("Error: El parser generó instrucciones inválidas o vacías.")
                return
        except Exception as e:
            print(f"Error al parsear el código: {e}")
            return

        try:
            manager = SimulatorManager(program_lines, active_indices=self.active_indices)
        except Exception as e:
            print(f"Error al inicializar el simulador: {e}")
            return

        # --- Integración con ExecutionHistory ---
        history = manager.history

        # Ejecutar cada procesador y actualizar interfaz
        for view_idx, sim_idx in enumerate(self.active_indices):
            cpu_name = manager.cpu_names[sim_idx]
            cpu = manager.cpus[view_idx]
            try:
                cpu.load_program(program_lines)
                cpu.run(modo="full", delay_seg=0)
                metrics = cpu.metrics

                ciclos = metrics.ciclos_totales
                inst = metrics.instrucciones_retiradas
                cpi = metrics.ciclos_totales / metrics.instrucciones_retiradas if metrics.instrucciones_retiradas else 0
                branch_total = metrics.branches_totales
                branch_acertados = metrics.branches_acertados

                if hasattr(metrics, "get_elapsed_time"):
                    tiempo = metrics.get_elapsed_time()
                elif hasattr(metrics, "elapsed_time"):
                    tiempo = metrics.elapsed_time
                else:
                    tiempo = 0.0

                pc = 0
                if hasattr(cpu, "pipeline") and hasattr(cpu.pipeline, "IF_ID"):
                    if hasattr(cpu.pipeline.IF_ID, "pc"):
                        pc = cpu.pipeline.IF_ID.pc
                    elif isinstance(cpu.pipeline.IF_ID, dict) and "pc" in cpu.pipeline.IF_ID:
                        pc = cpu.pipeline.IF_ID["pc"]
                elif hasattr(cpu, "pc"):
                    pc = cpu.pc

                print(f"\n--- Métricas para {cpu_name} ---")
                print(f"Ciclos totales: {ciclos}")
                print(f"Instrucciones retiradas: {inst}")
                print(f"CPI: {cpi:.2f}")
                print(f"Branches totales: {branch_total}")
                print(f"Branches acertados: {branch_acertados}")
                if metrics.branches_totales:
                    precision = (metrics.branches_acertados / metrics.branches_totales) * 100
                else:
                    precision = 0.0
                print(f"Precisión del predictor: {precision:.2f}%")

                self.update_metrics_sim(view_idx+1, ciclos, inst, cpi, branch_total, branch_acertados, precision)
                self.update_system_state_sim(view_idx+1, ciclos, tiempo, pc)

                # --- Guardar en historial de ejecuciones ---
                config = manager.cpu_configs[sim_idx]
                history.add_execution(
                    processor_name=cpu_name,
                    metrics=metrics,
                    config=config
                )

                # --- Actualizar registros en la interfaz gráfica ---
                if hasattr(cpu, "registers") and hasattr(cpu.registers, "dump"):
                    reg_dict = cpu.registers.dump()
                    self.update_registers_sim(view_idx+1, reg_dict)
                else:
                    self.update_registers_sim(view_idx+1, {f"x{i}": 0 for i in range(32)})

            except Exception as e:
                print(f"Error al ejecutar {cpu_name}: {e}")

        # --- Actualizar memoria en la interfaz gráfica después de la ejecución ---
        for view_idx, sim_idx in enumerate(self.active_indices):
            cpu = manager.cpus[view_idx]
            # dump devuelve {direccion: valor}
            if hasattr(cpu, "data_mem") and hasattr(cpu.data_mem, "dump"):
                mem_dict = cpu.data_mem.dump()
                self.update_memory_sim(view_idx+1, mem_dict)
            else:
                # Si no hay memoria, muestra todo en cero
                self.update_memory_sim(view_idx+1, {addr: 0 for addr in range(0, 4096, 4)})

    def _reset_simulation(self):
        """Reinicia la simulación, limpiando el código y el estado de las vistas."""
        print("Reiniciar simulación")
        # Detener ejecución rítmica si está corriendo
        self._stop_timed_exec()
        # 1. Borra el área de código
        self.code_space.delete("1.0", tk.END)

        # 2. Valores por defecto para las vistas de estado
        estado_pipeline_inicial = {
            "IF_ID": "nop",
            "ID_EX": "nop",
            "EX_MEM": "nop",
            "MEM_WB": "nop"
        }
        default_regs = [[i, 0] for i in range(32)]
        default_mem = [[i * 4, 0] for i in range(32)]
        default_metrics = (0, 0, 0, 0, 0, 0)
        default_ciclo = 0
        default_tiempo = 0.0
        default_pc = 0

        # 3. Refresca las vistas activas
        vistas_activas = [i for i, v in enumerate(self.active_views) if v]
        if len(vistas_activas) >= 1:
            self.view_status_1.set_view_name(f"Sim {vistas_activas[0] + 1}")
            self.view_status_1.update_system_state(default_ciclo, default_tiempo, default_pc)
            self.view_status_1.update_registers({f"x{i}": 0 for i in range(32)})
            self.view_status_1.update_memory(default_mem)
            self.view_status_1.update_metrics(*default_metrics)
            self.view_status_1.update_pipeline(estado_pipeline_inicial, ciclo=0)
        if len(vistas_activas) == 2:
            self.view_status_2.set_view_name(f"Sim {vistas_activas[1] + 1}")
            self.view_status_2.update_system_state(default_ciclo, default_tiempo, default_pc)
            self.view_status_2.update_registers({f"x{i}": 0 for i in range(32)})
            self.view_status_2.update_memory(default_mem)
            self.view_status_2.update_metrics(*default_metrics)
            self.view_status_2.update_pipeline(estado_pipeline_inicial, ciclo=0)

        # 4. Limpia historial
        self._history = {1: deque(maxlen=10), 2: deque(maxlen=10)}
        self._refresh_history_window()

    def highlight_for_sim(self, sim_number: int, unit_tag: str):
        """
        Resalta en la vista activa que corresponda a sim_number (1..4).
        Si la vista no está activa, no hace nada.
        """
        sim_idx = sim_number - 1
        frame = self._tabs.get(sim_idx)
        if frame:
            frame.highlight(unit_tag)

    def clear_highlight_for_sim(self, sim_number: int):
        """
        Limpia el resaltado en la vista activa que corresponda a sim_number (1..4).
        Si la vista no está activa, no hace nada.
        """
        sim_idx = sim_number - 1
        frame = self._tabs.get(sim_idx)
        if frame:
            frame.clear_highlights()

    def update_system_state_sim(self, view_number: int, ciclo: int, tiempo: float, pc: int):
        """
        Actualiza estado del sistema para la vista view_number (1 o 2).
        """
        # Forzar conversión a float y formatear a 4 decimales para asegurar visualización
        tiempo_str = f"{float(tiempo):.4f}"
        if view_number == 1 and self.active_views[self.active_indices[0]]:
            self.view_status_1.update_system_state(ciclo, float(tiempo_str), pc)
        elif view_number == 2 and len(self.active_indices) > 1 and self.active_views[self.active_indices[1]]:
            self.view_status_2.update_system_state(ciclo, float(tiempo_str), pc)
        else:
            print(f"Vista {view_number} no está activa o no existe.")

    def update_metrics_sim(self, view_number: int, ciclos, instrucciones, cpi, branches, branches_ok, precision):
        """
        Actualiza métricas para la vista view_number (1 o 2).
        """
        if view_number == 1 and self.active_views[self.active_indices[0]]:
            self.view_status_1.update_metrics(ciclos, instrucciones, cpi, branches, branches_ok, precision)
        elif view_number == 2 and len(self.active_indices) > 1 and self.active_views[self.active_indices[1]]:
            self.view_status_2.update_metrics(ciclos, instrucciones, cpi, branches, branches_ok, precision)
        else:
            print(f"Vista {view_number} no está activa o no existe.")

    def update_registers_sim(self, view_number: int, reg_matrix):
        """
        Actualiza los registros para la vista view_number (1 o 2).
        reg_matrix debe ser iterable de pares (reg_num, valor).
        """
        if view_number == 1 and self.active_views[self.active_indices[0]]:
            self.view_status_1.update_registers(reg_matrix)
        elif view_number == 2 and len(self.active_indices) > 1 and self.active_views[self.active_indices[1]]:
            self.view_status_2.update_registers(reg_matrix)
        else:
            print(f"Vista {view_number} no está activa o no existe.")

    def update_memory_sim(self, view_number: int, mem_matrix):
        """
        Actualiza la memoria para la vista view_number (1 o 2).
        mem_matrix debe ser iterable de pares (direccion, valor).
        """
        if view_number == 1 and self.active_views[self.active_indices[0]]:
            self.view_status_1.update_memory(mem_matrix)
        elif view_number == 2 and len(self.active_indices) > 1 and self.active_views[self.active_indices[1]]:
            self.view_status_2.update_memory(mem_matrix)
        else:
            print(f"Vista {view_number} no está activa o no existe.")

    def update_pipeline_sim(self, view_number: int, pipeline_info: dict, ciclo: int):
        """
        Actualiza la sección pipeline de la vista view_number.
        pipeline_info debe tener las claves: IF_ID, ID_EX, EX_MEM, MEM_WB con strings para mostrar.
        """
        if view_number == 1 and self.active_views[self.active_indices[0]]:
            self.view_status_1.update_pipeline(pipeline_info, ciclo)
        elif view_number == 2 and len(self.active_indices) > 1 and self.active_views[self.active_indices[1]]:
            self.view_status_2.update_pipeline(pipeline_info, ciclo)
        else:
            print(f"Vista {view_number} no está activa o no existe.")

    def update_history(self, sim_number: int,
                       ciclos, instrucciones, cpi,
                       branches, branches_ok, precision):
        """
        Registra una nueva línea de métricas para el simulador indicado
        (sim_number: 1 ó 2). Mantiene sólo las 10 más recientes.
        """
        if sim_number not in (1, 2):
            return

        entry = (f"Cic:{ciclos}  Inst:{instrucciones}  "
                 f"CPI:{cpi:.2f}  B:{branches}/{branches_ok}  "
                 f"Prec:{precision:.1f}%")
        self._history[sim_number].appendleft(entry)  # guarda lo nuevo arriba
        self._refresh_history_window()

    """
    ======================================================================
                             Menú de configuración
    ======================================================================
    """

    def _create_menu_bar(self):
        menu_bar = tk.Menu(self)

        # ── Configuración ────────────────────────────────────────────
        config_menu = tk.Menu(menu_bar, tearoff=0)
        config_menu.add_command(label="Opciones de configuración",
                                command=self._open_config_window)
        menu_bar.add_cascade(label="Configuración", menu=config_menu)

        # ── Historial ────────────────────────────────────────────────
        menu_bar.add_command(label="Historial",
                             command=self._open_history_window)

        self.config(menu=menu_bar)

    def _open_config_window(self):
        # Ventana modal para escoger exactamente 2 vistas.
        cfg = tk.Toplevel(self)
        cfg.title("Opciones de configuración")
        cfg.geometry("400x250")
        cfg.grab_set()

        tk.Label(cfg,
                 text="Selecciona exactamente 2 sims:",
                 font=("Arial", 11, "bold")).pack(pady=(10, 5))

        # Variables ligadas al estado actual
        self._opt_vars = [tk.BooleanVar(value=v) for v in self.active_views]

        # Orden histórico de selección (las que ya estaban activas primero)
        self._selection_order = [i for i, v in enumerate(self.active_views) if v]

        textos = ["Sim 1 (sin unidad de riesgos)",
                  "Sim 2 (con unidad de riesgos )",
                  "Sim 3 (con predicción de saltos)",
                  "Sim 4 (con unidad de riesgos con predicción de saltos)"]
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
        # Guardar los índices seleccionados
        self.active_indices = [i for i, v in enumerate(new_selection) if v]
        self._history = {1: deque(maxlen=10), 2: deque(maxlen=10)}
        self._refresh_history_window()
        self._refresh_sim_views()
        window.destroy()

    def _open_history_window(self):
        """Muestra (o trae al frente) la ventana de historial."""
        if self._history_win and self._history_win.winfo_exists():
            self._history_win.deiconify()
            return

        # --- Leer historial desde archivo y filtrar por procesadores activos ---
        history = ExecutionHistory()
        all_entries = history.get_history()

        # Obtener los nombres de los procesadores seleccionados actualmente
        vistas_activas = [i for i, v in enumerate(self.active_views) if v]
        # Cambia a usar la variable de clase CPU_NAMES
        nombre_proc_1 = SimulatorManager.CPU_NAMES[vistas_activas[0]]
        nombre_proc_2 = SimulatorManager.CPU_NAMES[vistas_activas[1]]

        # Filtrar las últimas 10 ejecuciones para cada procesador seleccionado
        def filter_last_n(entries, proc_name, n=10):
            filtered = [e for e in reversed(entries) if e["processor"] == proc_name]
            return filtered[:n]

        filtered_1 = filter_last_n(all_entries, nombre_proc_1)
        filtered_2 = filter_last_n(all_entries, nombre_proc_2)

        # Guardar en self._history para que _refresh_history_window lo use
        def format_entry(entry):
            m = entry["metrics"]
            return (f"Cic:{m['ciclos_totales']}  Inst:{m['instrucciones_retiradas']}  "
                    f"CPI:{m['cpi']:.2f}  B:{m['branches_totales']}/{m['branches_acertados']}  "
                    f"Prec:{(m['branch_accuracy'] if m['branch_accuracy'] is not None else 0):.1f}%")

        self._history = {
            1: [format_entry(e) for e in filtered_1],
            2: [format_entry(e) for e in filtered_2]
        }

        win = tk.Toplevel(self)
        win.title("Historial de métricas (últimas 10)")
        win.geometry("700x260")
        win.resizable(True, True)
        self._history_win = win

        # ---- Canvas + scrollbar para poder crecer verticalmente ----
        canvas = tk.Canvas(win, borderwidth=0)
        vbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        vbar.pack(side="right", fill="y")

        holder = tk.Frame(canvas)
        holder.bind("<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=holder, anchor="nw")

        # ---- Dos columnas (una por vista) --------------------------
        nombre_sim_1 = self._sim_names[vistas_activas[0]]
        nombre_sim_2 = self._sim_names[vistas_activas[1]]

        self._hist_frames = {
            1: tk.LabelFrame(holder, text=nombre_sim_1, font=("Arial", 10, "bold")),
            2: tk.LabelFrame(holder, text=nombre_sim_2, font=("Arial", 10, "bold"))
        }

        self._hist_frames[1].grid(row=0, column=0, sticky="nw", padx=10, pady=5)
        self._hist_frames[2].grid(row=0, column=1, sticky="nw", padx=10, pady=5)

        # contenedores de labels para refresco rápido
        self._hist_labels = {1: [], 2: []}
        self._refresh_history_window()

    def _refresh_history_window(self):
        """Redibuja las dos columnas si la ventana existe."""
        if not (self._history_win and self._history_win.winfo_exists()):
            return

        for sim in (1, 2):
            # borra labels viejos
            for lbl in self._hist_labels[sim]:
                lbl.destroy()
            self._hist_labels[sim].clear()

            # crea labels con el contenido actual
            for i, line in enumerate(self._history[sim]):
                lbl = tk.Label(self._hist_frames[sim], text=line, anchor="w",
                               font=("Courier", 9))
                lbl.grid(row=i, column=0, sticky="w")
                self._hist_labels[sim].append(lbl)

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

        """PRUEBA HIGHLIGHT - Borrar despues

        tk.Button(bar, text="Test H1", command=self.highlight_test).pack(side="left")
        tk.Button(bar, text="Test H2", command=lambda: self.clear_highlight_for_sim(1)).pack(side="left")
        """
        
    '''PRUEBA HIGHLIGHT - Borrar despues
    def highlight_test(self):
        """Prueba de resaltado en la vista 1."""
        self.highlight_for_sim(1, "alu")
        self.highlight_for_sim(1, "register_file")
    '''


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

        estado_pipeline_inicial = {
            "IF_ID": "nop",
            "ID_EX": "nop",
            "EX_MEM": "nop",
            "MEM_WB": "nop"
        }

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
            # Actualiza estado inicial de vista 1
            self.view_status_1.update_system_state(0, 0.0, 0)
            self.view_status_1.update_registers([[i, 0] for i in range(32)])
            self.view_status_1.update_memory([[i * 4, 0] for i in range(32)])
            self.view_status_1.update_metrics(0, 0, 0, 0,0,0)
            self.view_status_1.update_pipeline(estado_pipeline_inicial, ciclo=0)
            if not self.view_status_1.winfo_ismapped():
                self.view_status_1.pack(fill="both", expand=True)
        else:
            if self.view_status_1.winfo_ismapped():
                self.view_status_1.pack_forget()

        if len(vistas_activas) == 2:
            self.view_status_2.set_view_name(f"Sim {vistas_activas[1] + 1}")
            # Actualiza estado inicial de vista 2
            self.view_status_2.update_system_state(0, 0.0, 0)
            self.view_status_2.update_registers([[i, 0] for i in range(32)])
            self.view_status_2.update_memory([[i * 4, 0] for i in range(32)])
            self.view_status_2.update_metrics(0, 0, 0, 0,0,0)
            self.view_status_2.update_pipeline(estado_pipeline_inicial, ciclo=0)
            if not self.view_status_2.winfo_ismapped():
                self.view_status_2.pack(fill="both", expand=True)
        else:
            if self.view_status_2.winfo_ismapped():
                self.view_status_2.pack_forget()