from typing import List, Dict
import pandas as pd


def exportar_iteraciones_excel(iteraciones: List[Dict], ruta: str) -> None:
    df = pd.DataFrame([{
        'i': fila.get('i'),
        'x_{n-1}': fila.get('x_prev'),
        'x_n': fila.get('x_curr'),
        'x_{n+1}': fila.get('x_next'),
        'f(x_{n-1})': fila.get('f_prev'),
        'f(x_n)': fila.get('f_curr'),
        'Error': fila.get('error'),
    } for fila in iteraciones])
    df.to_excel(ruta, index=False)
