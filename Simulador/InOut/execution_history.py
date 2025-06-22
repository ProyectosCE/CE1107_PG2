import os
import json
from typing import Any

class ExecutionHistory:
    """
    Buffer circular para almacenar las últimas ejecuciones de procesadores.
    Cada entrada contiene las métricas y la configuración del procesador.
    """
    def __init__(self, json_filename="execution_history.json", num_procs=1):
        self.json_path = os.path.join(os.path.dirname(__file__), json_filename)
        self.max_entries = 10 * num_procs
        self.buffer = self._load_history()

    def _load_history(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data[-self.max_entries:]
            except Exception:
                pass
        return []

    def add_execution(self, processor_name: str, metrics: Any, config: dict):
        """
        Agrega una ejecución al buffer.
        - processor_name: nombre del procesador (str)
        - metrics: objeto Metrics (de metrics.py)
        - config: configuración relevante del procesador (dict)
        """
        entry = {
            "processor": processor_name,
            "metrics": self._metrics_to_dict(metrics),
            "config": config
        }
        self.buffer.append(entry)
        if len(self.buffer) > self.max_entries:
            self.buffer = self.buffer[-self.max_entries:]
        self._save_history()

    def _metrics_to_dict(self, metrics):
        # Convierte el objeto Metrics a dict serializable
        return {
            "name": getattr(metrics, "name", ""),
            "ciclos_totales": getattr(metrics, "ciclos_totales", 0),
            "instrucciones_retiradas": getattr(metrics, "instrucciones_retiradas", 0),
            "branches_totales": getattr(metrics, "branches_totales", 0),
            "branches_acertados": getattr(metrics, "branches_acertados", 0),
            "cpi": (metrics.ciclos_totales / metrics.instrucciones_retiradas)
                if getattr(metrics, "instrucciones_retiradas", 0) else 0.0,
            "branch_accuracy": (
                (metrics.branches_acertados / metrics.branches_totales) * 100
                if getattr(metrics, "branches_totales", 0) else None
            )
        }

    def _save_history(self):
        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(self.buffer, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando historial de ejecuciones: {e}")

    def get_history(self):
        """Devuelve una copia del buffer de ejecuciones."""
        return list(self.buffer)

    def clear_history(self):
        """Borra el historial y el archivo JSON."""
        self.buffer = []
        try:
            if os.path.exists(self.json_path):
                os.remove(self.json_path)
        except Exception:
            pass
