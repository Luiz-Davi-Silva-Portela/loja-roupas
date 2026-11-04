// Aula 12: a vitrine ganha vida.
// A lista de produtos é o DADO; desenhar() é a TELA. Separados desde já.
// Na Aula 13 esta lista passa a vir da API (GET /produtos).

const produtos = [
  { nome: "Camiseta básica", preco: 39.9, tam: "M" },
  { nome: "Calça jeans", preco: 129.9, tam: "G" },
  { nome: "Moletom", preco: 159.9, tam: "P" },
];

const vitrine = document.querySelector("#vitrine");

function formatarPreco(valor) {
  return `R$ ${valor.toFixed(2).replace(".", ",")}`;
}

// Monta o cartão com createElement + textContent (e não innerHTML), para que
// um nome digitado pelo usuário nunca seja interpretado como código HTML.
function montarCard(p) {
  const art = document.createElement("article");
  art.className = "produto";

  const titulo = document.createElement("h3");
  titulo.textContent = p.nome;

  const preco = document.createElement("p");
  const destaque = document.createElement("strong");
  destaque.textContent = formatarPreco(p.preco);
  preco.append(destaque);

  const tamanho = document.createElement("p");
  tamanho.textContent = `Tamanho ${p.tam}`;

  art.append(titulo, preco, tamanho);
  return art;
}

function desenhar(lista) {
  vitrine.innerHTML = ""; // limpa antes: chamar de novo não duplica
  lista.forEach((p) => vitrine.append(montarCard(p)));
}

desenhar(produtos);
