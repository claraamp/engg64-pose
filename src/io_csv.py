"""Leitura e escrita do CSV de resultados, sempre no formato de convencoes.py."""

from __future__ import annotations

import os

import numpy as np
import pandas as pd

from convencoes import (
    COLUNAS_CSV,
    COLUNAS_POSE,
    CSV_DECIMAIS,
    CSV_ENCODING,
    CSV_SEPARADOR,
)


def nova_linha(video: str, k: int, fps: float) -> dict:
    """Linha de um quadro ainda sem detecção (inválida por padrão)."""
    linha = {c: np.nan for c in COLUNAS_CSV}
    linha.update(video=video, k=int(k), t_s=k / fps, valido=0)
    return linha


def validar(df: pd.DataFrame) -> None:
    """Falha cedo se o DataFrame não respeitar o contrato."""
    if list(df.columns) != COLUNAS_CSV:
        raise ValueError(f"Colunas erradas: {list(df.columns)}; esperado {COLUNAS_CSV}")
    if not df["valido"].isin([0, 1]).all():
        raise ValueError("'valido' deve ser 0 ou 1")
    invalidos = df["valido"] == 0
    if df.loc[invalidos, COLUNAS_POSE].notna().any().any():
        raise ValueError("Quadros inválidos devem ter as colunas de pose vazias (NaN)")
    validos = ~invalidos
    if df.loc[validos, COLUNAS_POSE].isna().any().any():
        raise ValueError("Quadros válidos precisam de todas as colunas de pose")
    th = df.loc[validos, "thetaI_rad"]
    if ((th <= -np.pi / 2 - 1e-9) | (th > np.pi / 2 + 1e-9)).any():
        raise ValueError("thetaI_rad fora de (−π/2, π/2]")
    psi = df.loc[validos, "psi_rad"]
    if ((psi <= -np.pi - 1e-9) | (psi > np.pi + 1e-9)).any():
        raise ValueError("psi_rad fora de (−π, π]")


def salvar(linhas: list[dict] | pd.DataFrame, caminho: str) -> pd.DataFrame:
    df = linhas if isinstance(linhas, pd.DataFrame) else pd.DataFrame(linhas)
    df = df[COLUNAS_CSV].astype({"k": int, "valido": int})
    validar(df)
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    df.to_csv(caminho, sep=CSV_SEPARADOR, index=False,
              float_format=CSV_DECIMAIS, encoding=CSV_ENCODING)
    return df


def carregar(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho, sep=CSV_SEPARADOR, encoding=CSV_ENCODING)
    validar(df)
    return df
