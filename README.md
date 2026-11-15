# ENGG64 — Estimação da pose de um robô móvel

Projeto final de Visão Computacional (ENGG64, UFBA, 2026.2). A partir de vídeos 4K de uma câmera fixa, o pipeline segmenta o marcador vermelho do robô, estima centroide e orientação na imagem e, pela homografia do plano do chão, obtém a pose (XW, YW, ψ) do robô no mundo.

**Integrantes:** Amanda Bastos de Melo Correia · Júlia Teixeira Gonçalves · Maria Clara Andrade

## Estrutura

```
src/
  convencoes.py    contrato: eixos, escala, unidades, colunas do CSV
  io_csv.py        salvar/carregar o CSV checando o contrato
  segmentacao.py   etapas 1–3 (Júlia)
  pose.py          etapas 4–5 (Clara)
  main.py          pipeline: vídeo -> CSV (Clara, com Júlia)
  avaliacao.py     métricas (Amanda)
  graficos.py      figuras do relatório (Amanda)
  csv_ficticio.py  CSV de mentira no formato certo, para testar métricas e gráficos
tests/             testes das convenções (pytest)
notebooks/         notebook para rodar no Colab
data/              vídeos e H.txt (vídeos fora do git)
results/           CSVs, .mat, figuras e vídeos gerados (fora do git)
report/            figuras finais para o relatório (o texto fica no Overleaf)
```

As convenções estão em [CONVENCOES.md](CONVENCOES.md). Leia antes de mexer no código.

## Instalação

```bash
git clone https://github.com/<usuario>/engg64-pose.git
cd engg64-pose
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                           # deve passar tudo
```

## Execução

1. Baixe os vídeos do Drive do grupo para `data/` (link: TODO).
2. Coloque a homografia do enunciado em `data/H.txt` (matriz 3×3, mundo em mm → imagem em px).
3. Rode:

```bash
python src/main.py data/<video>.mp4 --H data/H.txt
```

O CSV sai em `results/<video>_pose.csv`. Para testar gráficos antes do pipeline existir: `python src/csv_ficticio.py`.

## Entrega

Relatório (IEEEconf, até 6 páginas), código, este README, dois vídeos com sobreposição e os arquivos de resultados, num único .zip.
