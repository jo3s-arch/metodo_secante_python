from typing import List, Any
import tkinter as tk
from tkinter import ttk


class TablaIteraciones(ttk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=("i","xn_1","xn","xn1","fxn_1","fxn","error"), show="headings")
        self.tree.heading("i", text="i")
        self.tree.heading("xn_1", text="x_{n-1}")
        self.tree.heading("xn", text="x_n")
        self.tree.heading("xn1", text="x_{n+1}")
        self.tree.heading("fxn_1", text="f(x_{n-1})")
        self.tree.heading("fxn", text="f(x_n)")
        self.tree.heading("error", text="Error")
        # Configure column widths and anchors
        self.tree.column("i", width=60, anchor='center')
        self.tree.column("xn_1", width=140, anchor='e')
        self.tree.column("xn", width=140, anchor='e')
        self.tree.column("xn1", width=140, anchor='e')
        self.tree.column("fxn_1", width=140, anchor='e')
        self.tree.column("fxn", width=140, anchor='e')
        self.tree.column("error", width=120, anchor='e')
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side='right', fill='y')
        self.tree.pack(fill="both", expand=True)

    def cargar_datos(self, datos: List[dict]) -> None:
        self.limpiar()
        for fila in datos:
            self.tree.insert("", "end", values=(
                fila.get("i"),
                f"{fila.get('x_prev'):.8g}" if fila.get('x_prev') is not None else '',
                f"{fila.get('x_curr'):.8g}" if fila.get('x_curr') is not None else '',
                f"{fila.get('x_next'):.8g}" if fila.get('x_next') is not None else '',
                f"{fila.get('f_prev'):.8g}" if fila.get('f_prev') is not None else '',
                f"{fila.get('f_curr'):.8g}" if fila.get('f_curr') is not None else '',
                f"{fila.get('error'):.8g}" if fila.get('error') is not None else '',
            ))

    def limpiar(self) -> None:
        for i in self.tree.get_children():
            self.tree.delete(i)
