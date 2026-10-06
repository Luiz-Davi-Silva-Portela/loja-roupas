FRETE_FIXO = 15.0
FRETE_GRATIS_A_PARTIR_DE = 200.0


def total_carrinho(itens):
    total = 0
    for preco, quantidade in itens:
        total = total + preco * quantidade
    return total

from loja.calculos import total_carrinho
assert total_carrinho([]) == 0
assert total_carrinho([(10, 2)]) == 20

def frete(valor_da_compra):
    """Frete grátis a partir de R$ 200; abaixo disso, R$ 15."""
    if valor_da_compra >= FRETE_GRATIS_A_PARTIR_DE:
        return 0.0
    return FRETE_FIXO