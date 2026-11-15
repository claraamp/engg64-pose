"""Etapas 4–5 — pose na imagem, homografia e continuidade angular.

Responsável: Clara.

Entrada: máscara do marcador no quadro reduzido (saída de segmentacao.py).
Saída: valores das colunas uc_px, vc_px, thetaI_rad, XW_mm, YW_mm, psi_rad.
"""

from __future__ import annotations

import cv2
import numpy as np

from convencoes import ESCALA, para_original, wrap_pi


def pose_imagem(mascara: np.ndarray, escala: float = ESCALA) -> tuple[float, float, float]:
    """Etapa 4: centroide e orientação da elipse equivalente.

    Retorna (uc, vc, thetaI) com uc, vc já na resolução ORIGINAL.
    """
    m = cv2.moments(mascara, binaryImage=True)
    if m["m00"] == 0:
        raise ValueError("Máscara vazia")
    u_s = m["m10"] / m["m00"]
    v_s = m["m01"] / m["m00"]
    theta = 0.5 * np.arctan2(2 * m["mu11"], m["mu20"] - m["mu02"])
    if theta <= -np.pi / 2:  # garante (−π/2, π/2]
        theta += np.pi
    uc, vc = para_original(u_s, v_s, escala)
    return float(uc), float(vc), float(theta)


def imagem_para_mundo(u, v, H: np.ndarray):
    """Ponto(s) da imagem original -> plano do chão (mm), via H⁻¹ e normalização."""
    Hinv = np.linalg.inv(H)
    p = Hinv @ np.vstack([np.atleast_1d(u), np.atleast_1d(v), np.ones(np.size(u))])
    return p[0] / p[2], p[1] / p[2]


def pose_mundo(uc: float, vc: float, thetaI: float, H: np.ndarray, d_px: float = 50.0):
    """Etapa 5: (XW, YW) do centroide e ψ por dois pontos (Eqs. 4–6).

    O segundo ponto fica a `d_px` pixels do centroide na direção θI.
    O ψ devolvido ainda tem ambiguidade de 180° (ver resolver_ambiguidade).
    """
    # TODO(Clara, até 24/11): conferir com as Eqs. 4–6 do enunciado.
    u2 = uc + d_px * np.cos(thetaI)
    v2 = vc + d_px * np.sin(thetaI)
    X, Y = imagem_para_mundo([uc, u2], [vc, v2], H)
    psi = np.arctan2(Y[1] - Y[0], X[1] - X[0])
    return float(X[0]), float(Y[0]), float(wrap_pi(psi))


def resolver_ambiguidade(psi: float, psi_anterior: float | None, psi_inicial: float | None = None) -> float:
    """Escolhe entre ψ e ψ + π o mais próximo da referência.

    Referência = ψ do último quadro válido; no 1º quadro válido, `psi_inicial`
    (frente do robô definida à mão). TODO(Clara, até 29/11): tratar sequências
    longas de quadros inválidos.
    """
    ref = psi_anterior if psi_anterior is not None else psi_inicial
    if ref is None:
        return float(wrap_pi(psi))
    candidatos = np.array([psi, psi + np.pi])
    dist = np.abs(wrap_pi(candidatos - ref))
    return float(wrap_pi(candidatos[np.argmin(dist)]))
