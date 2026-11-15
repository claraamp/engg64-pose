# Convenções do projeto

Este arquivo e o `src/convencoes.py` são o contrato entre os módulos. O `.py` é a fonte da verdade; este texto só explica. Mudou alguma coisa aqui? Abra um PR e marque as outras duas.

## Coordenadas e ângulos

| Item | Convenção |
|---|---|
| Eixos da imagem | Origem no canto superior esquerdo, u → direita, v → baixo (padrão OpenCV) |
| Centro de pixel | Inteiro: o pixel (0, 0) cobre [−0,5; 0,5] |
| θI | A partir de +u, girando de +u para +v. Com v para baixo, θI positivo aparece **horário** na tela. Intervalo (−π/2, π/2] |
| Escala | Processamos quadros reduzidos por `ESCALA`, mas uc, vc no CSV estão **sempre em 3840 × 2160**. Converter só com `para_original()` / `para_reduzida()` |
| Homografia | `[u, v, 1]ᵀ ~ H · [XW, YW, 1]ᵀ`, de mundo (mm, ZW = 0) para imagem original (px). A pose usa H⁻¹. H fica em `data/H.txt` |
| ψ | Frente do robô a partir de +XW, em (−π, π], com a ambiguidade de 180° já resolvida. Para plotar, `np.unwrap` |
| Unidades | mm e rad nos arquivos; graus só nos rótulos dos gráficos |

## CSV de saída (um por vídeo, `results/<video>_pose.csv`)

```
video,k,t_s,valido,uc_px,vc_px,thetaI_rad,XW_mm,YW_mm,psi_rad
```

- `video`: nome do arquivo de vídeo sem extensão
- `k`: índice do quadro, começando em 0; `t_s = k / fps`
- `valido`: 1 ou 0. Quadro inválido tem as colunas de pose **vazias** (NaN), nunca 0
- Separador vírgula, ponto decimal, 6 casas, UTF-8, com cabeçalho
- Sempre gravar com `io_csv.salvar()` e ler com `io_csv.carregar()`: os dois checam o contrato e falham cedo

## Interfaces entre módulos

```
segmentacao.reduzir(quadro_bgr, escala)          -> quadro reduzido
segmentacao.segmentar(quadro)                    -> máscara uint8 0/255
segmentacao.limpar(mascara)                      -> máscara limpa
segmentacao.selecionar_marcador(mascara, estado) -> (máscara do marcador | None, estado)
pose.pose_imagem(mascara_marcador)               -> (uc, vc, thetaI)   uc, vc já em 3840×2160
pose.pose_mundo(uc, vc, thetaI, H)               -> (XW, YW, psi)      psi ainda ambíguo
pose.resolver_ambiguidade(psi, psi_anterior)     -> psi
```

## Git

- Ninguém commita direto na `main`. Cada tarefa vai numa branch e entra por PR, revisado por outra integrante.
- Branches: `<nome>/<tarefa>`, ex.: `julia/segmentacao-hsv`, `clara/homografia`, `amanda/graficos`.
- Commits curtos, em português, no imperativo: `adiciona rejeição da cruz por solidez`.
- Antes do PR: `pytest` passando.
- Vídeos e resultados não vão para o git (estão no `.gitignore`). Os vídeos ficam no Drive do grupo.

## Código

- Python 3.10+; nomes em português sem acento (`mascara`, `quadro`); docstring dizendo entrada, saída e unidade.
- Parâmetros (limiares, tamanho do elemento estruturante…) como constantes no topo do módulo, com um comentário do porquê: isso vira texto do relatório.
