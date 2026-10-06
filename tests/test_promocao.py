import pytest

from loja.carrinho import Carrinho
from loja.produto import Produto
from loja.promocao import Cupom, Percentual, SemPromocao


def carrinho_com(promocao):
    c = Carrinho(promocao)
    c.adicionar(Produto("Camiseta básica", 39.90, "M"), 3)
    c.adicionar(Produto("Calça jeans", 129.90, "G"))
    return c   # subtotal 249.60


@pytest.mark.parametrize("promocao, esperado", [
    (SemPromocao(), 249.60),    # frete grátis
    (Percentual(10), 224.64),   # ainda acima de 200
    (Cupom(100), 164.60),       # 149.60 + 15 de frete
])
def test_total_com_cada_promocao(promocao, esperado):
    assert carrinho_com(promocao).total == pytest.approx(esperado)


def test_percentual_fora_do_intervalo():
    with pytest.raises(ValueError):
        Percentual(120)


def test_cupom_negativo_nao_e_aceito():
    with pytest.raises(ValueError):
        Cupom(-5)
