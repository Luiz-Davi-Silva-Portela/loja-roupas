"""Testes das telas em front/: o pytest também confere a página.

O HTMLParser (da biblioteca padrão do Python) lê cada página e lista as tags.
Toda página da pasta front/ passa pelos mesmos testes (parametrize).
"""
from html.parser import HTMLParser
from pathlib import Path

import pytest

FRONT = Path(__file__).resolve().parent.parent / "front"
PAGINAS = sorted(FRONT.glob("*.html"))


class Leitor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.itens = []

    def handle_starttag(self, tag, attrs):
        self.itens.append((tag, dict(attrs)))


def ler(pagina):
    leitor = Leitor()
    leitor.feed(pagina.read_text(encoding="utf-8"))
    return leitor.itens


@pytest.fixture(params=PAGINAS, ids=lambda p: p.name)
def pagina(request):
    return request.param


def test_existe_a_vitrine():
    assert (FRONT / "index.html").exists()


def test_estrutura_semantica(pagina):
    nomes = [t for t, _ in ler(pagina)]
    for tag in ("header", "nav", "main", "footer"):
        assert tag in nomes, f"falta <{tag}>"
    assert nomes.count("main") == 1
    assert nomes.count("h1") == 1


def test_toda_imagem_tem_alt(pagina):
    for tag, atributos in ler(pagina):
        if tag == "img":
            assert "alt" in atributos
