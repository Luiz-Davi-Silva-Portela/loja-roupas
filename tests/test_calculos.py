import pytest

from loja.calculos import frete, total_carrinho


def test_carrinho_vazio_custa_zero():
    assert total_carrinho([]) == 0


def test_soma_preco_vezes_quantidade():
    # 1. preparar
    itens = [(39.90, 3), (129.90, 1)]
    # 2. agir
    total = total_carrinho(itens)
    # 3. conferir
    assert total == pytest.approx(249.60)


def test_frete_abaixo_de_200_custa_15():
    assert frete(199.99) == 15.0


def test_frete_a_partir_de_200_e_gratis():
    assert frete(200.00) == 0.0
    assert frete(350.00) == 0.0
