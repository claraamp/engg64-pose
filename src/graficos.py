"""Etapa 6 — figuras do relatório.

Responsável: Amanda. Ângulos ficam em rad no CSV e viram graus só aqui;
ψ é desenrolado com np.unwrap antes de plotar.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def psi_continuo_graus(df: pd.DataFrame) -> np.ndarray:
    """ψ desenrolado, em graus, só nos quadros válidos."""
    v = df[df["valido"] == 1]
    return np.degrees(np.unwrap(v["psi_rad"].to_numpy()))


# TODO(Amanda): temporais de uc, vc, θI; temporais de XW, YW, ψ;
# trajetória XW × YW com início, fim e setas; validade por quadro.
