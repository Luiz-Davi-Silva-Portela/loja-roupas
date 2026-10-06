import pytest

from loja.carrinho import Carrinho
from loja.produto import Calca, Camiseta


def test_camiseta_herda_a_validacao_do_produto():
    with pytest.raises(ValueError):
        Camiseta("Camiseta básica", -10, "M", "curta")


def test_manga_invalida():
    with pytest.raises(ValueError):
        Camiseta("Camiseta básica", 39.90, "M", "regata")


def test_carrinho_aceita_camiseta():
    c = Carrinho()
    c.adicionar(Camiseta("Camiseta básica", 39.90, "M", "curta"))
    assert c.quantidade_de_pecas == 1


def test_descricao_da_calca():
    calca = Calca("Calça jeans", 129.90, "G", "slim")
    assert calca.descricao() == "Calça jeans G: R$ 129.90 · slim"
