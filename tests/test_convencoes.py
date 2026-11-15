import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cv2  # noqa: E402

import io_csv  # noqa: E402
import pose  # noqa: E402
from convencoes import para_original, para_reduzida, wrap_pi  # noqa: E402


def test_escala_ida_e_volta():
    u, v = np.array([0.0, 1919.5, 3839.0]), np.array([0.0, 1079.5, 2159.0])
    us, vs = para_reduzida(u, v, 0.25)
    u2, v2 = para_original(us, vs, 0.25)
    assert np.allclose(u, u2) and np.allclose(v, v2)


def test_centro_da_imagem_reduzida_vai_para_centro_original():
    # 960×540 -> centro (479.5, 269.5) deve virar (1919.5, 1079.5)
    u, v = para_original(479.5, 269.5, 0.25)
    assert np.isclose(u, 1919.5) and np.isclose(v, 1079.5)


def test_wrap_pi_intervalo():
    a = wrap_pi(np.array([-np.pi, np.pi, 3 * np.pi, -3 * np.pi / 2]))
    assert np.allclose(a, [np.pi, np.pi, np.pi, np.pi / 2])


def _retangulo(theta_graus, escala=1.0):
    m = np.zeros((540, 960), np.uint8)
    caixa = ((480, 270), (200, 60), theta_graus)
    cv2.fillPoly(m, [cv2.boxPoints(caixa).astype(np.int32)], 255)
    return m


@pytest.mark.parametrize("graus", [0, 30, -30, 60, 89])
def test_thetaI_segue_convencao(graus):
    # cv2.boxPoints usa o mesmo sentido (+u para +v), então θI ≈ ângulo do retângulo
    _, _, th = pose.pose_imagem(_retangulo(graus), escala=1.0)
    assert np.isclose(np.degrees(th), graus, atol=1.5)
    assert -np.pi / 2 < th <= np.pi / 2


def test_homografia_ida_e_volta():
    H = np.array([[0.9, 0.05, 1900], [0.02, -0.9, 1100], [1e-6, 2e-6, 1.0]])
    X, Y = np.array([0.0, 500.0, -1200.0]), np.array([0.0, 300.0, 700.0])
    p = H @ np.vstack([X, Y, np.ones(3)])
    u, v = p[0] / p[2], p[1] / p[2]
    X2, Y2 = pose.imagem_para_mundo(u, v, H)
    assert np.allclose(X, X2) and np.allclose(Y, Y2)


def test_ambiguidade_escolhe_mais_proximo():
    assert np.isclose(pose.resolver_ambiguidade(-3.0, psi_anterior=0.2), wrap_pi(np.pi - 3.0))
    assert np.isclose(pose.resolver_ambiguidade(0.1, psi_anterior=0.2), 0.1)


def test_csv_ficticio_respeita_contrato(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    import csv_ficticio
    df = csv_ficticio.gerar(n=120)
    df2 = io_csv.carregar("results/ficticio_pose.csv")
    assert len(df2) == len(df) == 120


def test_validar_rejeita_invalido_com_pose(tmp_path):
    linha = io_csv.nova_linha("x", 0, 30.0)
    linha["XW_mm"] = 1.0
    with pytest.raises(ValueError):
        io_csv.salvar([linha], str(tmp_path / "x.csv"))
