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


def test_todo_campo_tem_label(pagina):
    itens = ler(pagina)
    rotulos = {a["for"] for t, a in itens if t == "label" and a.get("for")}
    for tag, atributos in itens:
        if tag in ("input", "select", "textarea") and atributos.get("type") not in ("hidden", "submit"):
            assert atributos.get("id") in rotulos, f"campo sem label: {atributos}"


def test_titulos_em_ordem(pagina):
    niveis = [int(t[1]) for t, _ in ler(pagina) if t in ("h1", "h2", "h3", "h4", "h5", "h6")]
    assert niveis[0] == 1
    for anterior, atual in zip(niveis, niveis[1:]):
        assert atual <= anterior + 1, f"o título pulou de h{anterior} para h{atual}"


def test_idioma_e_viewport(pagina):
    itens = ler(pagina)
    html = next(a for t, a in itens if t == "html")
    assert html.get("lang") == "pt-BR"
    metas = [a for t, a in itens if t == "meta"]
    assert any(m.get("name") == "viewport" for m in metas)


def test_estilo_ligado_e_existente(pagina):
    links = [a for t, a in ler(pagina) if t == "link" and a.get("rel") == "stylesheet"]
    assert links, "a página não liga nenhum CSS"
    for link in links:
        assert (FRONT / link["href"]).exists()


def test_cadastro_tem_os_campos_do_post():
    cadastro = FRONT / "cadastro.html"
    assert cadastro.exists()
    nomes = {a.get("name") for t, a in ler(cadastro) if t in ("input", "select")}
    assert {"tipo", "nome", "preco", "tamanho"} <= nomes


def test_script_existe_e_fica_no_fim_do_body(pagina):
    itens = ler(pagina)
    nomes = [t for t, _ in itens]
    for posicao, (tag, atributos) in enumerate(itens):
        if tag == "script":
            assert (FRONT / atributos["src"]).exists()
            # o script roda depois de o navegador criar os elementos (ou usa defer)
            assert "defer" in atributos or posicao > nomes.index("footer")


def test_ids_usados_pelo_javascript_existem_nas_paginas():
    """Evita o clássico 'null' do querySelector: o id escrito no app.js existe no HTML."""
    import re

    ids_no_js = set(re.findall(r'querySelector\("#([\w-]+)"\)', (FRONT / "app.js").read_text(encoding="utf-8")))
    ids_nas_paginas = {a["id"] for p in PAGINAS for _, a in ler(p) if "id" in a}
    assert ids_no_js, "o app.js não usa nenhum id?"
    assert ids_no_js <= ids_nas_paginas, f"ids sem elemento: {ids_no_js - ids_nas_paginas}"


def test_cadastro_tem_aviso_e_vitrine_para_o_javascript():
    ids = {a["id"] for _, a in ler(FRONT / "cadastro.html") if "id" in a}
    assert {"form-produto", "aviso", "vitrine", "busca"} <= ids
