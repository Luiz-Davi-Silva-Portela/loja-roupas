import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from api import app, obter_sessao, popular_se_vazio
from loja.banco import criar_tabelas, engine_em_memoria
from loja.repositorio import RepositorioProdutos
from loja.servico import ServicoCatalogo

cliente = TestClient(app)


@pytest.fixture(autouse=True)
def banco_de_teste():
    engine = engine_em_memoria()
    criar_tabelas(engine)
    with Session(engine) as sessao:
        popular_se_vazio(ServicoCatalogo(RepositorioProdutos(sessao)))

    def sessao_de_teste():
        with Session(engine) as sessao:
            yield sessao

    app.dependency_overrides[obter_sessao] = sessao_de_teste
    cliente.delete("/carrinho")
    yield
    app.dependency_overrides.clear()


def test_vitrine_tem_tres_produtos():
    resposta = cliente.get("/produtos")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 3


def test_produto_inexistente_da_404():
    resposta = cliente.get("/produtos/99")
    assert resposta.status_code == 404


def test_filtro_por_tamanho():
    resposta = cliente.get("/produtos", params={"tamanho": "M"})
    nomes = [p["nome"] for p in resposta.json()]
    assert nomes == ["Camiseta básica"]


def test_quantidade_zero_da_422():
    resposta = cliente.post("/carrinho/itens", json={"produto_id": 1, "quantidade": 0})
    assert resposta.status_code == 422


def test_adicionar_item_da_201():
    resposta = cliente.post("/carrinho/itens", json={"produto_id": 1, "quantidade": 3})
    assert resposta.status_code == 201
    assert resposta.json()["pecas_no_carrinho"] == 3


def test_total_com_promocao_sem_frete():
    cliente.post("/carrinho/itens", json={"produto_id": 1, "quantidade": 3})
    cliente.post("/carrinho/itens", json={"produto_id": 2, "quantidade": 1})
    assert cliente.get("/carrinho/total").json() == {
        "pecas": 4, "subtotal": 249.6, "total": 224.64}


def test_total_abaixo_de_200_paga_frete():
    cliente.post("/carrinho/itens", json={"produto_id": 1, "quantidade": 1})
    assert cliente.get("/carrinho/total").json()["total"] == 50.91


def test_cadastrar_produto_da_201_e_aparece_no_catalogo():
    novo = {"nome": "Boné", "preco": 49.90, "tamanho": "M"}
    resposta = cliente.post("/produtos", json=novo)
    assert resposta.status_code == 201
    assert resposta.json()["id"] == 4
    assert cliente.get("/produtos/4").json()["nome"] == "Boné"


def test_nome_repetido_da_409():
    repetido = {"nome": "Moletom", "preco": 99.90, "tamanho": "P"}
    assert cliente.post("/produtos", json=repetido).status_code == 409


def test_tamanho_invalido_da_422():
    invalido = {"nome": "Boné", "preco": 49.90, "tamanho": "XL"}
    assert cliente.post("/produtos", json=invalido).status_code == 422


def test_alterar_e_remover_produto():
    alterado = cliente.put("/produtos/3", json={"nome": "Moletom", "preco": 139.90, "tamanho": "P"})
    assert alterado.status_code == 200
    assert alterado.json()["preco"] == 139.90
    assert cliente.delete("/produtos/3").status_code == 204
    assert cliente.get("/produtos/3").status_code == 404
