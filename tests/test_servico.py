import pytest
from sqlmodel import Session

from loja.banco import criar_tabelas, engine_em_memoria
from loja.repositorio import RepositorioProdutos
from loja.servico import (DadosInvalidos, ProdutoJaExiste,
                          ProdutoNaoEncontrado, ServicoCatalogo)

CAMISETA = {"tipo": "Camiseta", "nome": "Camiseta básica",
            "preco": 39.90, "tamanho": "M", "manga": "curta"}
CALCA = {"tipo": "Calca", "nome": "Calça jeans",
         "preco": 129.90, "tamanho": "G", "modelagem": "reta"}


@pytest.fixture
def servico():
    engine = engine_em_memoria()
    criar_tabelas(engine)
    with Session(engine) as sessao:
        yield ServicoCatalogo(RepositorioProdutos(sessao))


def test_nome_repetido_nao_entra(servico):
    servico.cadastrar(CAMISETA)
    with pytest.raises(ProdutoJaExiste):
        servico.cadastrar(CAMISETA)


def test_regra_do_dominio_vira_dados_invalidos(servico):
    with pytest.raises(DadosInvalidos):
        servico.cadastrar({**CAMISETA, "preco": 0})


def test_tipo_desconhecido_e_invalido(servico):
    with pytest.raises(DadosInvalidos):
        servico.cadastrar({**CAMISETA, "tipo": "Sapato"})


def test_buscar_inexistente(servico):
    with pytest.raises(ProdutoNaoEncontrado):
        servico.buscar(99)


def test_cadastrar_devolve_o_produto_com_id(servico):
    produto = servico.cadastrar(CAMISETA)
    assert produto["id"] == 1
    assert produto["nome"] == "Camiseta básica"


def test_atualizar_muda_o_preco(servico):
    servico.cadastrar(CAMISETA)
    atualizado = servico.atualizar(1, {**CAMISETA, "preco": 49.90})
    assert atualizado["preco"] == 49.90
    assert servico.buscar(1)["preco"] == 49.90


def test_atualizar_para_nome_de_outro_produto_da_conflito(servico):
    servico.cadastrar(CAMISETA)
    servico.cadastrar(CALCA)
    with pytest.raises(ProdutoJaExiste):
        servico.atualizar(2, {**CALCA, "nome": "Camiseta básica"})
