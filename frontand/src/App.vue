<script setup>
import logoImg from '@/assets/Imagens/logo.png';
import tractorImg from '@/assets/Imagens/tractor.png';
import venenoImg from '@/assets/Imagens/veneno.png';
import veneno1Img from '@/assets/Imagens/veneno1.png';

import { ref, computed, watch, onMounted } from 'vue';

const usuarioLogado = ref(localStorage.getItem('usuarioLogado') === 'true' || false);
const estaNaPaginaInicial = ref(!usuarioLogado.value);
const mostrarLoginModal = ref(false);
const mostrarCadastroInicialModal = ref(false); // Nova modal para escolher o tipo de cadastro
const mostrarCadastroRevendedorModal = ref(false); // Modal de cadastro para revendedor
const mostrarCadastroLojaModal = ref(false); // Modal de cadastro para loja
const loginEmail = ref('');
const loginSenha = ref('');

// Campos do formulário de revendedor
const revendedorNome = ref('');
const revendedorCidade = ref('');
const revendedorEstado = ref('');
const revendedorEmail = ref('');
const revendedorCpf = ref('');
const revendedorTelefoneCelular = ref('');
const revendedorDataNascimento = ref('');
const revendedorCep = ref('');
const revendedorRua = ref('');
const revendedorNumeroCasa = ref('');
const revendedorComplemento = ref('');
const revendedorBairro = ref('');
const revendedorIdLoja = ref('');

// Campos do formulário de loja
const lojaCep = ref('');
const lojaCnpj = ref('');
const lojaNomeFantasia = ref('');
const lojaRazaoSocial = ref('');
const lojaTelefone = ref('');
const lojaEmail = ref('');

const paginaAtual = ref(usuarioLogado.value ? 'produtos' : '');
const tituloPagina = ref('Produtos Agrícolas');
const mensagem = ref('Explore nossa variedade de produtos de alta qualidade para sua lavoura.');
const entradaTexto = ref('');
const entradaTexto2 = ref('');
const lista = ref([]);
const beneficios = ref(['Alta eficácia', 'Amplo espectro', 'Seguro para a cultura (se usado corretamente)']);
const produtos = ref([
    { id: 1, nome: 'Fertilizante Nitrogenado', descricao: '...', categoria: 'fertilizantes', preco: 55.90, disponivel: true, imagem: logoImg},
    { id: 2, nome: 'Semente de Milho Híbrido', descricao: '...', categoria: 'sementes', preco: 120.00, disponivel: true, imagem: tractorImg},
    { id: 3, nome: 'Herbicida Seletivo', descricao: '...', categoria: 'defensivos', preco: 89.50, disponivel: false, imagem: venenoImg },
    { id: 4, nome: 'Arado de Disco', descricao: '...', categoria: 'implementos', preco: 1500.00, disponivel: true, imagem: veneno1Img },
    { id: 5, nome: 'Semente de Soja RR', descricao: '...', categoria: 'sementes', preco: 150.00, disponivel: true, imagem: logoImg },
    { id: 6, nome: 'Fungicida Sistêmico', descricao: '...', categoria: 'defensivos', preco: 75.00, disponivel: false, imagem: tractorImg },
]);
const filtroCategoria = ref('');
const filtroPrecoMin = ref(null);
const filtroPrecoMax = ref(null);
const filtroDisponibilidade = ref('');
const produtoSelecionado = ref(null);
const isAdmin = ref(true);

const produtosFiltrados = computed(() => {
    return produtos.value.filter(produto => {
        const categoriaOk = !filtroCategoria.value || produto.categoria === filtroCategoria.value;
        const precoMinOk = filtroPrecoMin.value === null || produto.preco >= filtroPrecoMin.value;
        const precoMaxOk = filtroPrecoMax.value === null || produto.preco <= filtroPrecoMax.value;
        const disponibilidadeOk = filtroDisponibilidade.value === '' || produto.disponivel.toString() === filtroDisponibilidade.value;
        return categoriaOk && precoMinOk && precoMaxOk && disponibilidadeOk;
    });
});

const estaNaPaginaDeAutenticacao = computed(() => {
    return mostrarLoginModal.value || mostrarCadastroInicialModal.value || mostrarCadastroRevendedorModal.value || mostrarCadastroLojaModal.value || estaNaPaginaInicial.value;
});

watch(paginaAtual, (novaPagina) => {
    if (usuarioLogado.value) {
        estaNaPaginaInicial.value = false;
        mostrarLoginModal.value = false;
        mostrarCadastroInicialModal.value = false;
        mostrarCadastroRevendedorModal.value = false;
        mostrarCadastroLojaModal.value = false;
        switch (novaPagina) {
            case 'produtos':
                tituloPagina.value = 'Produtos Agrícolas';
                mensagem.value = 'Explore nossa variedade de produtos de alta qualidade para sua lavoura.';
                lista.value = [];
                break;
            case 'pedidos':
                tituloPagina.value = 'Gerenciamento de Pedidos';
                mensagem.value = 'Visualize e gerencie seus pedidos de forma eficiente.';
                lista.value = ['Pedido #123', 'Pedido #456', 'Pedido #789'];
                break;
            case 'vendas':
                tituloPagina.value = 'Relatório de Vendas';
                mensagem.value = 'Acompanhe o desempenho de suas vendas e gere relatórios detalhados.';
                lista.value = ['Venda Jan: R$ 10.000', 'Venda Fev: R$ 12.500', 'Venda Mar: R$ 11.800'];
                break;
            case 'sobre':
                tituloPagina.value = 'Sobre a Nossa Empresa';
                mensagem.value = 'Conheça nossa história, missão e valores.';
                lista.value = ['Fundação em 2020', 'Foco em sustentabilidade', 'Parcerias com produtores locais'];
                break;
            case 'contato':
                tituloPagina.value = 'Entre em Contato Conosco';
                mensagem.value = 'Estamos à disposição para tirar suas dúvidas e oferecer suporte.';
                lista.value = ['Email: contato@smartdash.com', 'Telefone: (XX) XXXXX-XXXX', 'Formulário de contato'];
                break;
            default:
                tituloPagina.value = 'SmartDash';
                mensagem.value = 'Bem-vindo ao seu painel de controle inteligente!';
                lista.value = [];
                break;
        }
        produtoSelecionado.value = null;
    } else {
        paginaAtual.value = '';
        estaNaPaginaInicial.value = true;
    }
});

watch(usuarioLogado, (novoStatus) => {
    localStorage.setItem('usuarioLogado', novoStatus);
    estaNaPaginaInicial.value = !novoStatus;
    if (novoStatus) {
        mostrarLoginModal.value = false;
        mostrarCadastroInicialModal.value = false;
        mostrarCadastroRevendedorModal.value = false;
        mostrarCadastroLojaModal.value = false;
        paginaAtual.value = 'produtos';
    } else {
        paginaAtual.value = '';
    }
});

function mostrarLogin() {
    estaNaPaginaInicial.value = false;
    mostrarLoginModal.value = true;
    mostrarCadastroInicialModal.value = false;
    mostrarCadastroRevendedorModal.value = false;
    mostrarCadastroLojaModal.value = false;
}

function mostrarCadastroInicial() {
    estaNaPaginaInicial.value = false;
    mostrarLoginModal.value = false;
    mostrarCadastroInicialModal.value = true;
    mostrarCadastroRevendedorModal.value = false;
    mostrarCadastroLojaModal.value = false;
}

function mostrarCadastroRevendedor() {
    mostrarCadastroInicialModal.value = false;
    mostrarCadastroRevendedorModal.value = true;
    mostrarCadastroLojaModal.value = false;
}

function mostrarCadastroLoja() {
    mostrarCadastroInicialModal.value = false;
    mostrarCadastroRevendedorModal.value = false;
    mostrarCadastroLojaModal.value = true;
}

function login() {
    if (loginEmail.value === 'teste@email.com' && loginSenha.value === '123456') {
        usuarioLogado.value = true;
        loginEmail.value = '';
        loginSenha.value = '';
    } else {
        alert('Credenciais inválidas.');
    }
}

function cadastrarRevendedor() {
    console.log('Cadastro de Revendedor:', {
        nome: revendedorNome.value,
        cidade: revendedorCidade.value,
        estado: revendedorEstado.value,
        email: revendedorEmail.value,
        cpf: revendedorCpf.value,
        telefoneCelular: revendedorTelefoneCelular.value,
        dataNascimento: revendedorDataNascimento.value,
        cep: revendedorCep.value,
        rua: revendedorRua.value,
        numeroCasa: revendedorNumeroCasa.value,
        complemento: revendedorComplemento.value,
        bairro: revendedorBairro.value,
        idLoja: revendedorIdLoja.value,
    });
    alert('Cadastro de revendedor realizado com sucesso! Faça login.');
    mostrarCadastroRevendedorModal.value = false;
    mostrarLoginModal.value = true;
    // Limpar os campos do formulário de revendedor
    revendedorNome.value = '';
    revendedorCidade.value = '';
    revendedorEstado.value = '';
    revendedorEmail.value = '';
    revendedorCpf.value = '';
    revendedorTelefoneCelular.value = '';
    revendedorDataNascimento.value = '';
    revendedorCep.value = '';
    revendedorRua.value = '';
    revendedorNumeroCasa.value = '';
    revendedorComplemento.value = '';
    revendedorBairro.value = '';
    revendedorIdLoja.value = '';
}

function cadastrarLoja() {
    console.log('Cadastro de Loja:', {
        cep: lojaCep.value,
        cnpj: lojaCnpj.value,
        nomeFantasia: lojaNomeFantasia.value,
        razaoSocial: lojaRazaoSocial.value,
        telefone: lojaTelefone.value,
        email: lojaEmail.value,
    });
    alert('Cadastro de loja realizado com sucesso! Faça login.');
    mostrarCadastroLojaModal.value = false;
    mostrarLoginModal.value = true;
    // Limpar os campos do formulário de loja
    lojaCep.value = '';
    lojaCnpj.value = '';
    lojaNomeFantasia.value = '';
    lojaRazaoSocial.value = '';
    lojaTelefone.value = '';
    lojaEmail.value = '';
}

function logout() {
    usuarioLogado.value = false;
    paginaAtual.value = '';
    estaNaPaginaInicial.value = true;
}

function navegarPara(pagina) {
    if (usuarioLogado.value) {
        paginaAtual.value = pagina;
        produtoSelecionado.value = null;
    }
}

function selecionarProduto(produto) {
    produtoSelecionado.value = produto;
}

onMounted(() => {
    if (usuarioLogado.value) {
        paginaAtual.value = 'produtos';
        estaNaPaginaInicial.value = false;
    }
});
</script>

<template>
    <header v-if="!estaNaPaginaInicial && usuarioLogado">
        <div>
            SmartDash
        </div>
        <nav>
            <a href="#" :class="{ active: paginaAtual === 'produtos' }" @click.prevent="navegarPara('produtos')">Produtos</a>
            <a href="#" :class="{ active: paginaAtual === 'pedidos' }" @click.prevent="navegarPara('pedidos')">Pedidos</a>
            <a href="#" :class="{ active: paginaAtual === 'vendas' }" @click.prevent="navegarPara('vendas')">Vendas</a>
            <a href="#" :class="{ active: paginaAtual === 'sobre' }" @click.prevent="navegarPara('sobre')">Sobre Nós</a>
            <a href="#" :class="{ active: paginaAtual === 'contato' }" @click.prevent="navegarPara('contato')">Contato</a>
            <button @click="logout">Sair</button>
        </nav>
    </header>

    <section v-if="estaNaPaginaInicial" class="pagina-inicial">
        <h1>Bem-vindo ao SmartDash</h1>
        <p>Seu painel de controle inteligente para gestão agrícola.</p>
        <div class="auth-buttons">
            <button @click="mostrarLogin">Login</button>
            <button @click="mostrarCadastroInicial">Criar Conta</button>
        </div>
    </section>

    <section v-if="mostrarLoginModal" class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="login">
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="loginEmail" required>
            </div>
            <div class="form-group">
                <label for="password">Senha:</label>
                <input type="password" id="password" v-model="loginSenha" required>
            </div>
            <div class="form-group">
                <button type="submit">Entrar</button>
            </div>
            <div class="link-cadastro">
                <a href="#" @click.prevent="mostrarCadastroInicial">Não tem uma conta? Cadastre-se</a>
            </div>
        </form>
    </section>

    <section v-if="mostrarCadastroInicialModal" class="cadastro-inicial-container">
        <h2>Como você gostaria de se cadastrar?</h2>
        <div class="cadastro-options">
            <button @click="mostrarCadastroRevendedor">Revendedor</button>
            <button @click="mostrarCadastroLoja">Loja</button>
        </div>
        <div class="link-login">
            <a href="#" @click.prevent="mostrarLogin">Já tem uma conta? Faça login</a>
        </div>
    </section>

    <section v-if="mostrarCadastroRevendedorModal" class="cadastro-revendedor-container">
        <h2>Cadastro de Revendedor</h2>
        <form @submit.prevent="cadastrarRevendedor">
            <div class="form-group">
                <label for="revendedorNome">Nome Completo:</label>
                <input type="text" id="revendedorNome" v-model="revendedorNome" required>
            </div>
            <div class="form-group">
                <label for="revendedorCidade">Cidade:</label>
                <input type="text" id="revendedorCidade" v-model="revendedorCidade" required>
            </div>
            <div class="form-group">
                <label for="revendedorEstado">Estado:</label>
                <input type="text" id="revendedorEstado" v-model="revendedorEstado" required>
            </div>
            <div class="form-group">
                <label for="revendedorEmail">Email:</label>
                <input type="email" id="revendedorEmail" v-model="revendedorEmail" required>
            </div>
            <div class="form-group">
                <label for="revendedorCpf">CPF:</label>
                <input type="text" id="revendedorCpf" v-model="revendedorCpf" required>
            </div>
            <div class="form-group">
                <label for="revendedorTelefoneCelular">Telefone Celular:</label>
                <input type="tel" id="revendedorTelefoneCelular" v-model="revendedorTelefoneCelular" required>
            </div>
            <div class="form-group">
                <label for="revendedorDataNascimento">Data de Nascimento:</label>
                <input type="date" id="revendedorDataNascimento" v-model="revendedorDataNascimento" required>
            </div>
            <div class="form-group">
                <label for="revendedorCep">CEP:</label>
                <input type="text" id="revendedorCep" v-model="revendedorCep" required>
            </div>
            <div class="form-group">
                <label for="revendedorRua">Rua:</label>
                <input type="text" id="revendedorRua" v-model="revendedorRua" required>
            </div>
            <div class="form-group">
                <label for="revendedorNumeroCasa">Número da Casa:</label>
                <input type="text" id="revendedorNumeroCasa" v-model="revendedorNumeroCasa" required>
            </div>
            <div class="form-group">
                <label for="revendedorComplemento">Complemento:</label>
                <input type="text" id="revendedorComplemento" v-model="revendedorComplemento">
            </div>
            <div class="form-group">
                <label for="revendedorBairro">Bairro:</label>
                <input type="text" id="revendedorBairro" v-model="revendedorBairro" required>
            </div>
            <div class="form-group">
                <label for="revendedorIdLoja">ID da Loja:</label>
                <input type="text" id="revendedorIdLoja" v-model="revendedorIdLoja">
            </div>
            <div class="form-group">
                <button type="submit">Cadastrar como Revendedor</button>
            </div>
            <div class="link-cadastro">
                <a href="#" @click.prevent="mostrarCadastroInicial">Voltar para a escolha de cadastro</a>
            </div>
        </form>
    </section>

    <section v-if="mostrarCadastroLojaModal" class="cadastro-loja-container">
        <h2>Cadastro de Loja</h2>
        <form @submit.prevent="cadastrarLoja">
            <div class="form-group">
                <label for="lojaNomeFantasia">Nome Fantasia:</label>
                <input type="text" id="lojaNomeFantasia" v-model="lojaNomeFantasia" required>
            </div>
            <div class="form-group">
                <label for="lojaRazaoSocial">Razão Social:</label>
                <input type="text" id="lojaRazaoSocial" v-model="lojaRazaoSocial" required>
            </div>
            <div class="form-group">
                <label for="lojaCnpj">CNPJ:</label>
                <input type="text" id="lojaCnpj" v-model="lojaCnpj" required>
            </div>
            <div class="form-group">
                <label for="lojaCep">CEP:</label>
                <input type="text" id="lojaCep" v-model="lojaCep" required>
            </div>
            <div class="form-group">
                <label for="lojaTelefone">Telefone:</label>
                <input type="tel" id="lojaTelefone" v-model="lojaTelefone" required>
            </div>
            <div class="form-group">
                <label for="lojaEmail">Email:</label>
                <input type="email" id="lojaEmail" v-model="lojaEmail" required>
            </div>
            <div class="form-group">
                <button type="submit">Cadastrar como Loja</button>
            </div>
            <div class="link-cadastro">
                <a href="#" @click.prevent="mostrarCadastroInicial">Voltar para a escolha de cadastro</a>
            </div>
        </form>
    </section>

    <div class="container" v-if="paginaAtual === 'produtos' && usuarioLogado">
        <h1>Catálogo de Produtos</h1>

        <div class="filtros">
            <label for="categoria">Categoria:</label>
            <select id="categoria" v-model="filtroCategoria">
                <option value="">Todas</option>
                <option value="fertilizantes">Fertilizantes</option>
                <option value="sementes">Sementes</option>
                <option value="defensivos">Defensivos</option>
                <option value="implementos">Implementos</option>
            </select>

            <label for="precoMin">Preço Mínimo:</label>
            <input type="number" id="precoMin" v-model="filtroPrecoMin">

            <label for="precoMax">Preço Máximo:</label>
            <input type="number" id="precoMax" v-model="filtroPrecoMax">

            <label for="disponibilidade">Disponibilidade:</label>
            <select id="disponibilidade" v-model="filtroDisponibilidade">
                <option value="">Todas</option>
                <option value="true">Em Estoque</option>
                <option value="false">Esgotados</option>
            </select>
        </div>

        <div class="produto-lista">
            <div v-for="produto in produtosFiltrados" :key="produto.id" class="produto-item">
                <img :src="produto.imagem" :alt="produto.nome">
                <h3>{{ produto.nome }}</h3>
                <p class="preco">R$ {{ produto.preco.toFixed(2) }}</p>
                <button @click="selecionarProduto(produto)">Ver Detalhes</button>
                <button v-if="isAdmin">Editar</button>
            </div>
        </div>


        <div v-if="produtoSelecionado" class="detalhes-produto">
            <h2>Detalhes do Produto</h2>
            <h3>{{ produtoSelecionado.nome }}</h3>
            <p>{{ produtoSelecionado.descricao }}</p>
            <p>Categoria: {{ produtoSelecionado.categoria }}</p>
            <p>Disponibilidade: {{ produtoSelecionado.disponivel ? 'Em estoque' : 'Esgotado' }}</p>
        </div>
    </div>

    <div class="container" v-else-if="paginaAtual === 'pedidos' && usuarioLogado">
        <h1>Gerenciamento de Pedidos</h1>
        <ul>
            <li v-for="pedido in lista">{{ pedido }}</li>
        </ul>
    </div>

    <div class="container" v-else-if="paginaAtual === 'vendas' && usuarioLogado">
        <h1>Relatório de Vendas</h1>
        <ul>
            <li v-for="venda in lista">{{ venda }}</li>
        </ul>
    </div>

    <div class="container" v-else-if="paginaAtual === 'sobre' && usuarioLogado">
        <h1>Sobre a Nossa Empresa</h1>
        <p>{{ mensagem }}</p>
        <ul>
            <li v-for="item in lista">{{ item }}</li>
        </ul>
    </div>

    <div class="container" v-else-if="paginaAtual === 'contato' && usuarioLogado">
        <h1>Entre em Contato Conosco</h1>
        <p>{{ mensagem }}</p>
        <ul>
            <li v-for="info in lista">{{ info }}</li>
        </ul>
    </div>

    <section v-if="usuarioLogado" class="rodape">
        <p>&copy; 2025 Desenvolvido por Ana Luiza, Andreza, Fernanda, Gustavo, Maria Eduarda e Vitor Hugo</p>
    </section>
</template>

<style scoped>
/* Estilos gerais */
body {
    font-family: sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
    color: #333;
}

.container {
    max-width: 960px;
    margin: 20px auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1, h2, h3 {
    color: #2c3e50;
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
    color: #555;
    font-weight: bold;
}

input[type="text"],
input[type="email"],
input[type="password"],
input[type="date"],
input[type="tel"],
input[type="number"],
select {
    width: calc(100% - 12px);
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}

button {
    background-color: #5cb85c;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #4cae4c;
}

.form-group {
    margin-bottom: 15px;
}

.link-cadastro, .link-login {
    margin-top: 10px;
    font-size: 0.9em;
}

.link-cadastro a, .link-login a {
    color: #007bff;
    text-decoration: none;
}

.link-cadastro a:hover, .link-login a:hover {
    text-decoration: underline;
}

/* Estilos do cabeçalho */
header {
    background-color: #333;
    color: white;
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

header div {
    font-size: 1.5em;
    font-weight: bold;
}

header nav a {
    color: white;
    text-decoration: none;
    margin-left: 20px;
    padding: 8px 10px;
    border-radius: 4px;
    transition: background-color 0.3s ease;
}

header nav a:hover,
header nav a.active {
    background-color: #555;
}

header nav button {
    background-color: #d9534f;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1em;
    margin-left: 20px;
    transition: background-color 0.3s ease;
}

header nav button:hover {
    background-color: #c9302c;
}

/* Estilos da página inicial */
.pagina-inicial {
    text-align: center;
    padding: 40px 20px;
}

.pagina-inicial h1 {
    font-size: 2.5em;
    margin-bottom: 20px;
}

.pagina-inicial p {
    font-size: 1.1em;
    color: #666;
    margin-bottom: 30px;
}

.pagina-inicial .auth-buttons button {
    margin: 0 10px;
}

/* Estilos dos containers de autenticação */
.login-container,
.cadastro-inicial-container,
.cadastro-revendedor-container,
.cadastro-loja-container {
    max-width: 400px;
    margin: 30px auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.cadastro-inicial-container h2 {
    margin-bottom: 20px;
}

.cadastro-options {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-bottom: 20px;
}

.cadastro-options button {
    flex-grow: 1;
}

/* Estilos da lista de produtos */
.produto-lista {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.produto-item {
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 15px;
    text-align: center;
}

.produto-item img {
    max-width: 100%;
    height: auto;
    margin-bottom: 10px;
    border-radius: 4px;
}

.produto-item h3 {
    font-size: 1.2em;
    margin-bottom: 5px;
}

.produto-item .preco {
    color: #5cb85c;
    font-weight: bold;
    margin-bottom: 10px;
}

/* Estilos dos filtros */
.filtros {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
    align-items: center;
}

.filtros label {
    font-weight: normal;
}

/* Estilos dos detalhes do produto */
.detalhes-produto {
    margin-top: 20px;
    padding: 15px;
    background-color: #f9f9f9;
    border-radius: 4px;
    border: 1px solid #eee;
    text-align: left;
}

.detalhes-produto h2 {
    font-size: 1.5em;
    margin-bottom: 10px;
}

.detalhes-produto h3 {
    font-size: 1.3em;
    margin-bottom: 8px;
}





.detalhes-produto p {
    color: #575353;
    line-height: 1.6;
    margin-bottom: 10px;
}

/* Estilos do rodapé */
.rodape {
    text-align: center;
    padding: 20px;
    background-color: #333;
    color: white;
    font-size: 0.9em;
    position: sticky;
    bottom: 0;
    width: 100%;
}
</style>
