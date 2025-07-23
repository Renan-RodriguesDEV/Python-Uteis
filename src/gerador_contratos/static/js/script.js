//  Máscara de entrada
function aplicarMascaraCPF(valor) {
  return valor
    .replace(/\D/g, "")
    .replace(/(\d{3})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
}

function aplicarMascaraRG(valor) {
  return valor
    .replace(/\D/g, "")
    .replace(/(\d{2})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d{1})$/, "$1-$2");
}

const camposCPF = [
  document.getElementById("cpf_vendedor"),
  document.getElementById("cpf_comprador"),
];
const camposRG = [
  document.getElementById("rg_vendedor"),
  document.getElementById("rg_comprador"),
];

camposCPF.forEach((campo) => {
  campo.addEventListener("input", (e) => {
    e.target.value = aplicarMascaraCPF(e.target.value);
  });
});

camposRG.forEach((campo) => {
  campo.addEventListener("input", (e) => {
    e.target.value = aplicarMascaraRG(e.target.value);
  });
});
