"""Pipeline completo: vídeo -> CSV de pose por quadro.

Uso:
    python src/main.py data/video1.mp4 --H data/H.txt [--max-quadros 300]

Integração: Clara (com Júlia). Marco 1 em 01/12.
"""

from __future__ import annotations

import argparse
import os
import time

import cv2
import numpy as np

import io_csv
import pose
import segmentacao
from convencoes import ESCALA, caminho_csv


def processar(caminho_video: str, H: np.ndarray, max_quadros: int | None = None,
              psi_inicial: float | None = None):
    video = os.path.splitext(os.path.basename(caminho_video))[0]
    cap = cv2.VideoCapture(caminho_video)
    if not cap.isOpened():
        raise FileNotFoundError(caminho_video)
    fps = cap.get(cv2.CAP_PROP_FPS)

    linhas, estado, psi_ant, tempos = [], None, None, []
    k = 0
    while max_quadros is None or k < max_quadros:
        ok, quadro = cap.read()
        if not ok:
            break
        t0 = time.perf_counter()
        linha = io_csv.nova_linha(video, k, fps)

        reduzido = segmentacao.reduzir(quadro, ESCALA)
        mascara = segmentacao.limpar(segmentacao.segmentar(reduzido))
        marcador, estado = segmentacao.selecionar_marcador(mascara, estado)

        if marcador is not None:
            uc, vc, thI = pose.pose_imagem(marcador)
            X, Y, psi = pose.pose_mundo(uc, vc, thI, H)
            psi = pose.resolver_ambiguidade(psi, psi_ant, psi_inicial)
            psi_ant = psi
            linha.update(valido=1, uc_px=uc, vc_px=vc, thetaI_rad=thI,
                         XW_mm=X, YW_mm=Y, psi_rad=psi)

        tempos.append(time.perf_counter() - t0)
        linhas.append(linha)
        k += 1
    cap.release()

    df = io_csv.salvar(linhas, caminho_csv(video))
    print(f"{video}: {len(df)} quadros, {df['valido'].mean():.1%} válidos, "
          f"{1000 * np.mean(tempos):.1f} ms/quadro -> {caminho_csv(video)}")
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--H", default="data/H.txt", help="matriz 3×3 mundo(mm) -> imagem(px)")
    ap.add_argument("--max-quadros", type=int, default=None)
    ap.add_argument("--psi-inicial", type=float, default=None, help="frente do robô no 1º quadro (rad)")
    a = ap.parse_args()
    processar(a.video, np.loadtxt(a.H), a.max_quadros, a.psi_inicial)
