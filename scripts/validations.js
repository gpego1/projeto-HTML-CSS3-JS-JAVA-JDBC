
async function validarCPF(cpf) {
    try {
        const response = await axios.get(`https://api.invertexto.com/v1/validator?token=17609%7CyxPXBjmNiqMlmQ3zTR4ioI1wd67YHdPZ&value=${cpf}&type=cpf`);
        return response.data.valid; 
    } catch (error) {
        console.error("Erro ao validar o CPF:", error);
        return false;
    }
}

// Validação dos campos
async function validarFormulario(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const idade = document.getElementById("idade").value.trim();
    const cpf = document.getElementById("cpf").value.trim();
    const endereco = document.getElementById("endereco").value.trim();
    const email = document.getElementById("email").value.trim();
    const telefone = document.getElementById("telefone").value.trim();

    if (!/^[a-zA-Z]+ [a-zA-Z]+$/.test(nome)) {
        alert("O nome deve conter pelo menos nome e sobrenome.");
        return;
    }
    if (isNaN(idade) || idade < 0 || idade > 120) {
        alert("A idade deve ser um número válido entre 0 e 120.");
        return;
    }
    const cpfValido = await validarCPF(cpf);
    if (!cpfValido) {
        alert("O CPF informado é inválido.");
        return;
    }
    if (endereco.length < 5) {
        alert("O endereço deve conter pelo menos 5 caracteres.");
        return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert("O e-mail informado é inválido.");
        return;
    }
    if (!/^\d{10,11}$/.test(telefone)) {
        alert("O telefone deve conter 10 ou 11 dígitos.");
        return;
    }
    alert("Formulário válido! Enviando...");
    document.getElementById("formCadastro").submit();
}