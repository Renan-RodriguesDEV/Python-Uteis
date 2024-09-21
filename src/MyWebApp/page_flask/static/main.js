function logar() {
  var email = document.getElementById("email").value;
  var senha = document.getElementById("senha").value;

  if (String(email).endsWith("@gmail.com") && senha === "123456") {
    alert("Login realizado com sucesso!");
    window.location.href = "/"; // Redirecionar para a página home
  } else {
    alert("Email ou senha inválidos!");
  }
}
