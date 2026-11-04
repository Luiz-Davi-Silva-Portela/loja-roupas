# loja-roupas
![testes](https://github.com/Luiz-Davi-Silva-Portela/loja-roupas/actions/workflows/testes.yml/badge.svg)

Sistema de uma loja de roupas: API (FastAPI + SQLite, em camadas) e as telas no navegador.

## Como rodar

**API**

```bash
pip install -r requirements.txt
uvicorn api:app --reload      # documentação em http://127.0.0.1:8000/docs
```

**Telas (`front/`)**

Abra `front/index.html` no navegador (duplo clique ou a extensão Live Server do VS Code).

| Página | O que faz |
| --- | --- |
| `front/index.html` | Vitrine: os cartões são desenhados por JavaScript e a busca filtra enquanto a pessoa digita |
| `front/cadastro.html` | Formulário de cadastro com os campos do `POST /produtos`, validação no `submit` e prévia da vitrine |

Por enquanto os produtos ficam dentro do `front/app.js`; na Aula 13 passam a vir da API (`fetch`).

## Testes

```bash
pytest
```

O `tests/test_front.py` confere as telas: HTML semântico, `alt` nas imagens, `label` em todo campo, títulos em ordem, `lang`/`viewport`, CSS ligado e os ids que o `app.js` usa.
