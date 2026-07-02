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
        self.tree.pack(fill="both", expand=True)

    def cargar_datos(self, datos: List[dict]) -> None:
        self.limpiar()
        for fila in datos:
            self.tree.insert("", "end", values=(
                fila.get("i"),
                fila.get("x_prev"),
                fila.get("x_curr"),
                fila.get("x_next"),
                fila.get("f_prev"),
                fila.get("f_curr"),
                fila.get("error"),
            ))

    def limpiar(self) -> None:
        for i in self.tree.get_children():
            self.tree.delete(i)
