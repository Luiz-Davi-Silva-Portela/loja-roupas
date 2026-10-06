import pytest

from loja.carrinho import Carrinho
from loja.promocao import Cupom, Percentual, Promocao, SemPromocao


def test_promocao_abstrata_nao_nasce():
    with pytest.raises(TypeError):
        Promocao()


def test_promocao_sem_aplicar_nao_nasce():
    class BlackFriday(Promocao):
        def aplicar_desconto(self, subtotal):   # nome errado
            return subtotal * 0.5

    with pytest.raises(TypeError):
        BlackFriday()


def test_carrinho_recusa_quem_nao_segue_o_contrato():
    class Parecida:
        def aplicar(self, subtotal):
            return subtotal

    with pytest.raises(TypeError):
        Carrinho(Parecida())


@pytest.mark.parametrize("promocao", [SemPromocao(), Percentual(10), Cupom(50)])
def test_promocoes_reais_seguem_o_contrato(promocao):
    assert isinstance(promocao, Promocao)
