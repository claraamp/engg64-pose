"""
Convenções do projeto ENGG64 — estimação da pose do robô móvel.

Este arquivo é o CONTRATO entre os módulos. Ninguém muda colunas, unidades
ou sinais aqui sem avisar o grupo (e sem PR revisado pelas outras duas).

Resumo
------
Imagem
    - Origem no canto superior esquerdo; u -> direita, v -> baixo (padrão OpenCV).
    - Centro de pixel em coordenada inteira: o pixel (0, 0) cobre [-0.5, 0.5].
    - θI medido a partir de +u, no sentido de +u para +v. Como v aponta para
      baixo, θI positivo aparece HORÁRIO na tela.
    - θI vem de ½·atan2(2μ11, μ20 − μ02), portanto θI ∈ (−π/2, π/2].
Escala
    - Os quadros são processados reduzidos pelo fator ESCALA (definido pela
      Júlia na etapa 1). uc, vc no CSV são SEMPRE na resolução original
      3840×2160, porque é nela que a homografia H vale.
    - Converter com `para_original()` / `para_reduzida()` — nunca à mão.
    - θI não muda com escala uniforme (mesmo fator em u e v).
Mundo
    - H leva o plano do chão (XW, YW em mm, ZW = 0) para a imagem original
      (u, v em px): [u, v, 1]ᵀ ~ H · [XW, YW, 1]ᵀ. A pose usa H⁻¹.
    - XW, YW em mm; ψ em rad, ângulo da frente do robô a partir de +XW.
    - ψ no CSV fica em (−π, π], já com a ambiguidade de 180° resolvida.
      Para gráficos contínuos, usar np.unwrap na hora de plotar.
Unidades
    - Ângulos em rad nos arquivos; graus só nos rótulos dos gráficos.
Quadros inválidos
    - valido = 0 e as colunas numéricas de pose ficam vazias (NaN).
    - k e t_s são sempre preenchidos.
"""

from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------------
# Resolução e escala
# ---------------------------------------------------------------------------
LARGURA_ORIGINAL = 3840
ALTURA_ORIGINAL = 2160

# Fator de redução usado no processamento (ex.: 0.25 -> 960×540).
# TODO(Júlia, até 19/11): fixar o valor e justificar no relatório.
ESCALA = 0.25


def para_original(u_s, v_s, escala: float = ESCALA):
    """Coordenadas no quadro reduzido -> coordenadas em 3840×2160.

    Usa a convenção de centro de pixel do cv2.resize, que é a exata:
    u_orig = (u_s + 0.5) / escala − 0.5.
    """
    u_s = np.asarray(u_s, dtype=float)
    v_s = np.asarray(v_s, dtype=float)
    return (u_s + 0.5) / escala - 0.5, (v_s + 0.5) / escala - 0.5


def para_reduzida(u, v, escala: float = ESCALA):
    """Coordenadas em 3840×2160 -> coordenadas no quadro reduzido."""
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    return (u + 0.5) * escala - 0.5, (v + 0.5) * escala - 0.5


# ---------------------------------------------------------------------------
# Formato do CSV de saída (uma linha por quadro)
# ---------------------------------------------------------------------------
COLUNAS_CSV = [
    "video",       # str   identificador do vídeo (nome do arquivo sem extensão)
    "k",           # int   índice do quadro, começando em 0
    "t_s",         # float tempo do quadro em s: k / fps
    "valido",      # int   1 = detecção válida, 0 = inválida
    "uc_px",       # float centroide u na imagem ORIGINAL (px)
    "vc_px",       # float centroide v na imagem ORIGINAL (px)
    "thetaI_rad",  # float orientação na imagem, (−π/2, π/2]
    "XW_mm",       # float posição no mundo (mm)
    "YW_mm",       # float posição no mundo (mm)
    "psi_rad",     # float orientação no mundo, (−π, π], ambiguidade resolvida
]

COLUNAS_POSE = COLUNAS_CSV[4:]  # ficam NaN quando valido = 0

CSV_SEPARADOR = ","        # vírgula separa colunas
CSV_DECIMAIS = "%.6f"      # ponto decimal, 6 casas
CSV_ENCODING = "utf-8"


def caminho_csv(video: str) -> str:
    """Onde cada vídeo grava o seu CSV."""
    return f"results/{video}_pose.csv"


def wrap_pi(angulo):
    """Leva um ângulo (rad) para (−π, π]."""
    a = np.asarray(angulo, dtype=float)
    return np.pi - np.mod(np.pi - a, 2 * np.pi)
