"""Gera um CSV fictício no formato combinado, para a Amanda testar métricas e
gráficos antes do pipeline existir.

Uso:
    python src/csv_ficticio.py            # results/ficticio_pose.csv
"""

from __future__ import annotations

import numpy as np

import io_csv
from convencoes import caminho_csv, wrap_pi


def gerar(n: int = 900, fps: float = 30.0, taxa_invalidos: float = 0.08, seed: int = 0):
    rng = np.random.default_rng(seed)
    t = np.arange(n) / fps
    # trajetória em "8" no chão, em mm
    X = 1500 * np.sin(2 * np.pi * t / 30)
    Y = 800 * np.sin(4 * np.pi * t / 30)
    psi = np.arctan2(np.gradient(Y), np.gradient(X))
    # imagem: só uma relação plausível, não é a homografia real
    uc = 1920 + 0.9 * X + rng.normal(0, 2, n)
    vc = 1080 - 0.9 * Y + rng.normal(0, 2, n)
    thI = wrap_pi(-psi)
    thI = np.where(thI > np.pi / 2, thI - np.pi, thI)
    thI = np.where(thI <= -np.pi / 2, thI + np.pi, thI)

    valido = rng.random(n) > taxa_invalidos
    linhas = []
    for k in range(n):
        linha = io_csv.nova_linha("ficticio", k, fps)
        if valido[k]:
            linha.update(valido=1, uc_px=uc[k], vc_px=vc[k], thetaI_rad=thI[k],
                         XW_mm=X[k], YW_mm=Y[k], psi_rad=float(wrap_pi(psi[k])))
        linhas.append(linha)
    return io_csv.salvar(linhas, caminho_csv("ficticio"))


if __name__ == "__main__":
    df = gerar()
    print(f"{len(df)} linhas -> {caminho_csv('ficticio')}")
