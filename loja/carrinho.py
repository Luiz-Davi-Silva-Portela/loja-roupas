from .calculos import frete, total_carrinho
from .produto import Produto
from .promocao import Promocao, SemPromocao


class CarrinhoFinalizadoError(Exception):
    pass


class Carrinho:
    def __init__(self, promocao=None):
        if promocao is not None and not isinstance(promocao, Promocao):
            raise TypeError("a promoção precisa seguir o contrato Promocao")
        self._itens = []   # pares (produto, quantidade)
        self._finalizado = False
        self.promocao = promocao or SemPromocao()

    def adicionar(self, produto, quantidade=1):
        if self._finalizado:
            raise CarrinhoFinalizadoError("carrinho finalizado não recebe peças")
        if not isinstance(produto, Produto):
            raise TypeError("só é possível adicionar um Produto")
        if quantidade <= 0:
            raise ValueError("quantidade deve ser positiva")
        self._itens.append((produto, quantidade))

    @property
    def itens(self):
        return list(self._itens)

    @property
    def quantidade_de_pecas(self):
        return sum(quantidade for _, quantidade in self._itens)

    @property
    def subtotal(self):
        return total_carrinho([(p.preco, q) for p, q in self._itens])

    @property
    def total(self):
        com_desconto = self.promocao.aplicar(self.subtotal)
        return com_desconto + frete(com_desconto)

    def finalizar(self):
        if not self._itens:
            raise ValueError("não é possível finalizar um carrinho vazio")
        self._finalizado = True
