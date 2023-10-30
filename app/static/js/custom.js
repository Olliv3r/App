const author = document.getElementById("author");
const alias = document.getElementById("alias");
const nameRepo = document.getElementById("name_repository");
const link = document.getElementById("link");
const typeInstall = document.getElementById("type_install");

// Preenche os campos: autor, apelido e nome do repositório dinamicamente
link.addEventListener("change", (event) => {
  if (typeInstall.value == "git") {
    author.value = event.target.value.split("/")[3];
    alias.value = event.target.value.split("/")[4];
    nameRepo.value = event.target.value.split("/")[4];
  }
});