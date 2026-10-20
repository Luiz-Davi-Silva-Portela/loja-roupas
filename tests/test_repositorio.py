import pytest
from sqlmodel import Session

from loja.banco import criar_engine, criar_tabelas, engine_em_memoria
from loja.produto import Calca, Camiseta, Produto
from loja.repositorio import RepositorioProdutos


@pytest.fixture
def repo():
    engine = engine_em_memoria()
    criar_tabelas(engine)
    with Session(engine) as sessao:
        yield RepositorioProdutos(sessao)


def test_adicionar_e_buscar_devolve_o_tipo_certo(repo):
    produto_id = repo.adicionar(Camiseta("Camiseta básica", 39.90, "M", "curta"))
    achado = repo.buscar(produto_id)
    assert isinstance(achado, Camiseta)
    assert achado.manga == "curta"


def test_buscar_inexistente_devolve_none(repo):
    assert repo.buscar(99) is None


def test_listar_filtra_por_tamanho_e_preco(repo):
    repo.adicionar(Camiseta("Camiseta básica", 39.90, "M", "curta"))
    repo.adicionar(Calca("Calça jeans", 129.90, "G", "reta"))
    repo.adicionar(Produto("Moletom", 159.90, "P"))
    assert [p.nome for _, p in repo.listar()] == [
        "Camiseta básica", "Calça jeans", "Moletom"]
    assert [p.nome for _, p in repo.listar(tamanho="M")] == ["Camiseta básica"]
    assert [p.nome for _, p in repo.listar(preco_max=130)] == [
        "Camiseta básica", "Calça jeans"]


def test_existe_nome_ignora_o_proprio_produto(repo):
    produto_id = repo.adicionar(Produto("Moletom", 159.90, "P"))
    assert repo.existe_nome("Moletom") is True
    assert repo.existe_nome("Moletom", exceto_id=produto_id) is False
    assert repo.existe_nome("Boné") is False


def test_atualizar_e_remover(repo):
    produto_id = repo.adicionar(Produto("Moletom", 159.90, "P"))
    assert repo.atualizar(produto_id, Produto("Moletom", 139.90, "M")) is True
    assert repo.buscar(produto_id).preco == 139.90
    assert repo.remover(produto_id) is True
    assert repo.buscar(produto_id) is None
    assert repo.remover(produto_id) is False


def test_dados_sobrevivem_ao_reinicio(tmp_path):
    url = f"sqlite:///{tmp_path / 'loja.db'}"
    engine = criar_engine(url)
    criar_tabelas(engine)
    with Session(engine) as sessao:
        RepositorioProdutos(sessao).adicionar(Produto("Moletom", 159.90, "P"))
    engine.dispose()
    outro = criar_engine(url)
    with Session(outro) as sessao:
        assert RepositorioProdutos(sessao).buscar(1).nome == "Moletom"
