"""Etapa 6 — métricas: taxa de válidos, seleções incorretas, tempo por quadro.

Responsável: Amanda. Lê os CSVs com io_csv.carregar().
"""

from __future__ import annotations

import pandas as pd


def taxa_validos(df: pd.DataFrame) -> float:
    return float(df["valido"].mean())


def selecoes_incorretas(df: pd.DataFrame, ground_truth: pd.DataFrame, tol_px: float = 20.0) -> int:
    """Conta quadros válidos cujo centroide está a mais de `tol_px` do GT."""
    raise NotImplementedError  # TODO(Amanda)
