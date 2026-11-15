"""Etapas 1–3 — leitura, segmentação, morfologia e seleção do marcador.

Responsável: Júlia.

Contrato com pose.py: `selecionar_marcador` devolve uma máscara binária
(uint8, 0/255) do TAMANHO DO QUADRO REDUZIDO contendo só o marcador, ou None
quando não houver detecção válida no quadro.
"""

from __future__ import annotations

import numpy as np


def reduzir(quadro_bgr: np.ndarray, escala: float) -> np.ndarray:
    """Etapa 1: redimensiona o quadro 3840×2160 pelo fator `escala`."""
    raise NotImplementedError  # TODO(Júlia)


def segmentar(quadro_bgr: np.ndarray) -> np.ndarray:
    """Etapa 2: máscara binária (uint8, 0/255) dos pixels vermelhos."""
    raise NotImplementedError  # TODO(Júlia)


def limpar(mascara: np.ndarray) -> np.ndarray:
    """Etapa 2: abertura/fechamento morfológico."""
    raise NotImplementedError  # TODO(Júlia)


def selecionar_marcador(mascara: np.ndarray, estado: dict | None) -> tuple[np.ndarray | None, dict]:
    """Etapa 3: escolhe o componente do marcador e rejeita a cruz do piso.

    `estado` guarda o que for útil do quadro anterior (ex.: último centroide).
    Retorna (mascara_do_marcador ou None, novo_estado).
    """
    raise NotImplementedError  # TODO(Júlia)
