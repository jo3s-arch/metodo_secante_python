from typing import Callable
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sympy import symbols, lambdify
import numpy as np

x = symbols('x')


def crear_evaluador(expr: str) -> Callable[[float], float]:
    """
    Crea una función segura f(x) a partir de la expresión en cadena expr usando sympy.
    """
    if not expr:
        raise ValueError("La expresión está vacía")
    transformations = (standard_transformations + (implicit_multiplication_application,))
    parsed = parse_expr(expr, transformations=transformations, evaluate=True)
    func = lambdify(x, parsed, modules=["numpy"])

    def f_val(v):
        # Acepta escalares y numpy arrays
        try:
            return func(v)
        except Exception:
            # fallback a evaluación escalar
            if isinstance(v, (list, tuple, np.ndarray)):
                return np.array([float(func(float(t))) for t in v])
            return float(func(float(v)))

    return f_val
