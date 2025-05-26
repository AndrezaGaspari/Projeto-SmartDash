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
const revendedorSenha = ref(''); // Novo campo senha para revendedor

// Campos do formulário de loja
const lojaCep = ref('');
const lojaCnpj = ref('');
const lojaNomeFantasia = ref('');
const lojaRazaoSocial = ref('');
const lojaTelefone = ref('');
const lojaEmail = ref('');
const lojaSenha = ref(''); // Novo campo senha para loja

const paginaAtual = ref(usuarioLogado.value ? 'produtos' : '');
const tituloPagina = ref('Produtos Agrícolas');
const mensagem = ref('Explore nossa variedade de produtos de alta qualidade para sua lavoura.');
const entradaTexto = ref('');
const entradaTexto2 = ref('');
const lista = ref([]);
const beneficios = ref(['Alta eficácia', 'Amplo espectro', 'Seguro para a cultura (se usado corretamente)']);
const produtos = ref([
    { id: 1, nome: 'Fertilizante Nitrogenado', descricao: 'Fertilizante rico em nitrogênio para o crescimento vegetativo.', categoria: 'fertilizantes', preco: 55.90, disponivel: true, imagem: logoImg},
    { id: 2, nome: 'Semente de Milho Híbrido', descricao: 'Semente de milho de alta produtividade e resistência.', categoria: 'sementes', preco: 120.00, disponivel: true, imagem: tractorImg},
    { id: 3, nome: 'Herbicida Seletivo', descricao: 'Herbicida para controle de ervas daninhas sem prejudicar a cultura principal.', categoria: 'defensivos', preco: 89.50, disponivel: false, imagem: venenoImg },
    { id: 4, nome: 'Arado de Disco', descricao: 'Implemento agrícola robusto para preparo do solo.', categoria: 'implementos', preco: 1500.00, disponivel: true, imagem: veneno1Img },
    { id: 5, nome: 'Semente de Soja RR', descricao: 'Semente de soja geneticamente modificada para resistência a glifosato.', categoria: 'sementes', preco: 150.00, disponivel: true, imagem: logoImg },
    { id: 6, nome: 'Fungicida Sistêmico', descricao: 'Fungicida de ação sistêmica para proteção contra doenças fúngicas.', categoria: 'defensivos', preco: 75.00, disponivel: false, imagem: tractorImg },
]);
const filtroCategoria = ref('');
const filtroPrecoMin = ref(null);
const filtroPrecoMax = ref(null);
const filtroDisponibilidade = ref('');
const produtoSelecionado = ref(null);
const isAdmin = ref(true);
const pedidosRevendedor = ref([]);
const pedidosAprovacao = ref([
    { id: 'PR001', revendedor: 'Revendedor A', itens: [{ nome: 'Fertilizante Nitrogenado', quantidade: 2 }, { nome: 'Semente de Milho Híbrido', quantidade: 1 }], status: 'pendente' },
    { id: 'PR002', revendedor: 'Revendedor B', itens: [{ nome: 'Herbicida Seletivo', quantidade: 3 }], status: 'pendente' },
]);
const produtoEditando = ref(null);
const edicaoNome = ref('');
const edicaoPreco = ref(null);
// NOVAS REFS PARA EDIÇÃO DE PRODUTOS
const edicaoDescricao = ref('');
const edicaoCategoria = ref('');
const edicaoDisponivel = ref(true);
const edicaoImagem = ref('');


// Novos campos para cadastro de produto
const novoProdutoNome = ref('');
const novoProdutoDescricao = ref('');
const novoProdutoCategoria = ref('');
const novoProdutoPreco = ref(null);
const novoProdutoDisponivel = ref(true); // Ou false, dependendo do padrão
const novoProdutoImagem = ref(''); // URL da imagem ou importação

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
                tituloPagina.value = 'Catálogo de Produtos';
                mensagem.value = 'Selecione os produtos para revenda.';
                lista.value = [];
                produtoEditando.value = null; // Reset edição ao mudar de página
                break;
            case 'pedidos':
                tituloPagina.value = 'Meus Pedidos';
                mensagem.value = 'Acompanhe seus pedidos de revenda.';
                lista.value = pedidosRevendedor.value.map(pedido => `Pedido com ${pedido.itens ? pedido.itens.length : 1} item(s)`);
                produtoEditando.value = null;
                break;
            case 'aprovacoes':
                tituloPagina.value = 'Aprovação de Pedidos';
                mensagem.value = 'Aprove ou rejeite os pedidos dos revendedores.';
                lista.value = [];
                produtoEditando.value = null;
                break;
            case 'dashboard':
                tituloPagina.value = 'Dashboard de Vendas';
                mensagem.value = 'Métricas de vendas e desempenho.';
                lista.value = [];
                produtoEditando.value = null;
                break;
            case 'vendas':
                tituloPagina.value = 'Relatórios de Vendas';
                mensagem.value = 'Histórico e desempenho de suas vendas.';
                lista.value = ['Venda Jan: R$ 10.000', 'Venda Fev: R$ 12.500', 'Venda Mar: R$ 11.800'];
                produtoEditando.value = null;
                break;
            case 'cadastro-produto': // Nova página de cadastro de produto
                tituloPagina.value = 'Cadastro de Novo Produto';
                mensagem.value = 'Preencha os dados para adicionar um novo produto ao catálogo.';
                lista.value = [];
                produtoEditando.value = null;
                break;
            case 'sobre':
                tituloPagina.value = 'Sobre a Nossa Empresa';
                mensagem.value = 'Conheça nossa história, missão e valores.';
                lista.value = ['Fundação em 2020', 'Foco em sustentabilidade', 'Parcerias com produtores locais'];
                produtoEditando.value = null;
                break;
            case 'contato':
                tituloPagina.value = 'Entre em Contato Conosco';
                mensagem.value = 'Estamos à disposição para tirar suas dúvidas e oferecer suporte.';
                lista.value = ['Email: contato@smartdash.com', 'Telefone: (XX) XXXXX-XXXX', 'Formulário de contato'];
                produtoEditando.value = null;
                break;
            default:
                tituloPagina.value = 'SmartDash';
                mensagem.value = 'Bem-vindo ao seu painel de controle inteligente!';
                lista.value = [];
                produtoEditando.value = null;
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

async function cadastrarRevendedor() {
    console.log("Função cadastrarRevendedor chamada");

    try {
        const response = await fetch("http://127.0.0.1:8000/revendedores", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nome: revendedorNome.value,
                cidade: revendedorCidade.value,
                estado: revendedorEstado.value,
                email: revendedorEmail.value,
                senha: revendedorSenha.value,
                cpf: revendedorCpf.value,
                telefone: revendedorTelefoneCelular.value,
                data_nascimento: revendedorDataNascimento.value,
                cep: revendedorCep.value,
                rua: revendedorRua.value,
                numero_casa: Number(revendedorNumeroCasa.value),
                complemento: revendedorComplemento.value,
                bairro: revendedorBairro.value,
                fk_loja_id: Number(1)
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Erro ao cadastrar revendedor");
        }

        const data = await response.json();
        alert("Revendedor cadastrado com sucesso!");
        console.log(data);

        // Limpa o formulário
        revendedorNome.value = '';
        revendedorCidade.value = '';
        revendedorEstado.value = '';
        revendedorEmail.value = '';
        revendedorSenha.value = '';
        revendedorCpf.value = '';
        revendedorTelefoneCelular.value = '';
        revendedorDataNascimento.value = '';
        revendedorCep.value = '';
        revendedorRua.value = '';
        revendedorNumeroCasa.value = '';
        revendedorComplemento.value = '';
        revendedorBairro.value = '';
        revendedorIdLoja.value = '';

        mostrarCadastroRevendedorModal.value = false;
        mostrarLoginModal.value = true;

    } catch (error) {
        alert(`Erro: ${error.message}`);
    }
}


async function cadastrarLoja() {
    console.log("Função cadastrarLoja chamada");

    try {
        const response = await fetch("http://127.0.0.1:8000/lojas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                cep: lojaCep.value,
                cnpj: lojaCnpj.value,
                nome_fantasia: lojaNomeFantasia.value,
                razao_social: lojaRazaoSocial.value,
                telefone: lojaTelefone.value,
                email: lojaEmail.value,
                senha: lojaSenha.value
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Erro ao cadastrar loja");
        }

        const data = await response.json();
        alert("Loja cadastrada com sucesso!");
        console.log(data);

        // Limpa os campos do formulário
        lojaCep.value = '';
        lojaCnpj.value = '';
        lojaNomeFantasia.value = '';
        lojaRazaoSocial.value = '';
        lojaTelefone.value = '';
        lojaEmail.value = '';
        lojaSenha.value = '';

        mostrarCadastroLojaModal.value = false;
        mostrarLoginModal.value = true;

    } catch (error) {
        alert(`Erro: ${error.message}`);
    }
}
// Função de login
async function login() {
    try {
        const response = await fetch('http://localhost:8000/login', { 
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: loginEmail.value,
                senha: loginSenha.value,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.mensagem || 'Login bem-sucedido!'); 
            usuarioLogado.value = true;
            localStorage.setItem('usuarioLogado', 'true');
        } else {
            alert(data.detail || 'Erro no login: credenciais inválidas ou erro do servidor.'); 
        }
    } catch (error) {
        console.error('Erro na requisição de login:', error);
        alert('Erro ao conectar com o servidor.');
    }
}
// Nova função para cadastrar produto
function cadastrarProduto() {
    if (!novoProdutoNome.value || !novoProdutoCategoria.value || !novoProdutoPreco.value) {
        alert('Por favor, preencha nome, categoria e preço do produto.');
        return;
    }

    const novoId = produtos.value.length > 0 ? Math.max(...produtos.value.map(p => p.id)) + 1 : 1;
    produtos.value.push({
        id: novoId,
        nome: novoProdutoNome.value,
        descricao: novoProdutoDescricao.value,
        categoria: novoProdutoCategoria.value,
        preco: parseFloat(novoProdutoPreco.value),
        disponivel: novoProdutoDisponivel.value,
        imagem: novoProdutoImagem.value || logoImg // Usa a imagem fornecida ou uma padrão
    });

    alert('Produto cadastrado com sucesso!');
    // Limpa os campos do formulário
    novoProdutoNome.value = '';
    novoProdutoDescricao.value = '';
    novoProdutoCategoria.value = '';
    novoProdutoPreco.value = null;
    novoProdutoDisponivel.value = true;
    novoProdutoImagem.value = '';

    navegarPara('produtos'); // Volta para a lista de produtos após o cadastro
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

function adicionarAoPedido(produto) {
    pedidosRevendedor.value.push({ produtoId: produto.id, nome: produto.nome, preco: produto.preco, quantidade: 1 });
    alert(`${produto.nome} adicionado ao pedido.`);
}

function enviarPedido() {
    if (pedidosRevendedor.value.length > 0) {
        console.log('Pedido enviado:', pedidosRevendedor.value);
        alert('Pedido enviado para aprovação!');
        pedidosRevendedor.value = [];
        navegarPara('pedidos');
    } else {
        alert('Seu pedido está vazio.');
    }
}

function selecionarProduto(produto) {
    produtoSelecionado.value = produto;
}

function aprovarPedido(pedido) {
    alert(`Pedido ${pedido.id} aprovado.`);
    pedido.status = 'aprovado';
}

function rejeitarPedido(pedido) {
    alert(`Pedido ${pedido.id} rejeitado.`);
    pedido.status = 'rejeitado';
}

// FUNÇÃO EDITAR PRODUTO ATUALIZADA
function editarProduto(produto) {
    produtoEditando.value = produto;
    edicaoNome.value = produto.nome;
    edicaoPreco.value = produto.preco;
    edicaoDescricao.value = produto.descricao; // Novo
    edicaoCategoria.value = produto.categoria; // Novo
    edicaoDisponivel.value = produto.disponivel; // Novo
    edicaoImagem.value = produto.imagem; // Novo
}

// FUNÇÃO SALVAR EDIÇÃO PRODUTO ATUALIZADA
function salvarEdicaoProduto() {
    if (produtoEditando.value) {
        const index = produtos.value.findIndex(p => p.id === produtoEditando.value.id);
        if (index !== -1) {
            produtos.value[index].nome = edicaoNome.value;
            produtos.value[index].preco = parseFloat(edicaoPreco.value);
            produtos.value[index].descricao = edicaoDescricao.value; // Novo
            produtos.value[index].categoria = edicaoCategoria.value; // Novo
            produtos.value[index].disponivel = edicaoDisponivel.value; // Novo
            produtos.value[index].imagem = edicaoImagem.value || logoImg; // Novo
            produtoEditando.value = null;
            alert('Produto atualizado com sucesso!');
        }
    }
}

function cancelarEdicaoProduto() {
    produtoEditando.value = null;
}

function selecionarPedido(pedido) {
    produtoSelecionado.value = pedido;
}

onMounted(() => {
    if (usuarioLogado.value) {
        paginaAtual.value = 'produtos';
        estaNaPaginaInicial.value = false;
    }
});
</script>

<div id="app"></div>

<template>
    <header v-if="!estaNaPaginaInicial && usuarioLogado">
        <div>
            SmartDash
        </div>
        <nav>
            <a href="#" :class="{ active: paginaAtual === 'produtos' }" @click.prevent="navegarPara('produtos')">Produtos</a>
            <a href="#" :class="{ active: paginaAtual === 'pedidos' }" @click.prevent="navegarPara('pedidos')">Meus Pedidos</a>
            <a v-if="isAdmin" href="#" :class="{ active: paginaAtual === 'cadastro-produto' }" @click.prevent="navegarPara('cadastro-produto')">Cadastrar Produto</a>
            <a v-if="isAdmin" href="#" :class="{ active: paginaAtual === 'aprovacoes' }" @click.prevent="navegarPara('aprovacoes')">Aprovações</a>
            <a v-if="isAdmin" href="#" :class="{ active: paginaAtual === 'dashboard' }" @click.prevent="navegarPara('dashboard')">Dashboard</a>
            <a href="#" :class="{ active: paginaAtual === 'vendas' }" @click.prevent="navegarPara('vendas')">Relatórios</a>
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
                <label for="revendedorSenha">Senha:</label>
                <input type="password" id="revendedorSenha" v-model="revendedorSenha" required>
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
                <label for="lojaSenha">Senha:</label>
                <input type="password" id="lojaSenha" v-model="lojaSenha" required>
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
                <button @click="adicionarAoPedido(produto)">Adicionar ao Pedido</button>
                <button @click="selecionarProduto(produto)">Ver Detalhes</button>
                <button v-if="isAdmin" @click="editarProduto(produto)">Editar</button>
            </div>
        </div>

        <div v-if="pedidosRevendedor.length > 0" class="meu-pedido">
            <h2>Meu Pedido</h2>
            <ul>
                <li v-for="item in pedidosRevendedor" :key="item.produtoId">
                    {{ item.nome }} - R$ {{ item.preco.toFixed(2) }}
                </li>
            </ul>
            <button @click="enviarPedido">Enviar Pedido</button>
        </div>

        <div v-if="produtoSelecionado" class="detalhes-produto">
            <h2>Detalhes do Produto</h2>
            <h3>{{ produtoSelecionado.nome }}</h3>
            <p>{{ produtoSelecionado.descricao }}</p>
            <p>Categoria: {{ produtoSelecionado.categoria }}</p>
            <p>Disponibilidade: {{ produtoSelecionado.disponivel ? 'Em estoque' : 'Esgotado' }}</p>
        </div>

        <div v-if="produtoEditando" class="editar-produto">
            <h2>Editar Produto</h2>
            <div class="form-group">
                <label for="edicaoNome">Nome:</label>
                <input type="text" id="edicaoNome" v-model="edicaoNome" required>
            </div>
            <div class="form-group">
                <label for="edicaoDescricao">Descrição:</label>
                <textarea id="edicaoDescricao" v-model="edicaoDescricao"></textarea>
            </div>
            <div class="form-group">
                <label for="edicaoCategoria">Categoria:</label>
                <select id="edicaoCategoria" v-model="edicaoCategoria" required>
                    <option value="">Selecione uma categoria</option>
                    <option value="fertilizantes">Fertilizantes</option>
                    <option value="sementes">Sementes</option>
                    <option value="defensivos">Defensivos</option>
                    <option value="implementos">Implementos</option>
                </select>
            </div>
            <div class="form-group">
                <label for="edicaoPreco">Preço:</label>
                <input type="number" id="edicaoPreco" v-model="edicaoPreco" step="0.01" required>
            </div>
            <div class="form-group checkbox-group">
                <input type="checkbox" id="edicaoDisponivel" v-model="edicaoDisponivel">
                <label for="edicaoDisponivel">Disponível em Estoque</label>
            </div>
            <div class="form-group">
                <label for="edicaoImagem">URL da Imagem:</label>
                <input type="text" id="edicaoImagem" v-model="edicaoImagem">
            </div>
            <button @click="salvarEdicaoProduto">Salvar Edição</button>
            <button @click="cancelarEdicaoProduto">Cancelar</button>
        </div>
    </div>

    <div class="container" v-else-if="paginaAtual === 'cadastro-produto' && usuarioLogado && isAdmin">
        <h1>{{ tituloPagina }}</h1>
        <p>{{ mensagem }}</p>
        <form @submit.prevent="cadastrarProduto" class="form-cadastro-produto">
            <div class="form-group">
                <label for="novoProdutoNome">Nome do Produto:</label>
                <input type="text" id="novoProdutoNome" v-model="novoProdutoNome" required>
            </div>
            <div class="form-group">
                <label for="novoProdutoDescricao">Descrição:</label>
                <textarea id="novoProdutoDescricao" v-model="novoProdutoDescricao"></textarea>
            </div>
            <div class="form-group">
                <label for="novoProdutoCategoria">Categoria:</label>
                <select id="novoProdutoCategoria" v-model="novoProdutoCategoria" required>
                    <option value="">Selecione uma categoria</option>
                    <option value="fertilizantes">Fertilizantes</option>
                    <option value="sementes">Sementes</option>
                    <option value="defensivos">Defensivos</option>
                    <option value="implementos">Implementos</option>
                </select>
            </div>
            <div class="form-group">
                <label for="novoProdutoPreco">Preço:</label>
                <input type="number" id="novoProdutoPreco" v-model="novoProdutoPreco" step="0.01" required>
            </div>
             <div class="form-group checkbox-group">
                <input type="checkbox" id="novoProdutoDisponivel" v-model="novoProdutoDisponivel">
                <label for="novoProdutoDisponivel">Disponível em Estoque</label>
             </div>
             <div class="form-group">
                <label for="novoProdutoImagem">URL da Imagem:</label>
                <input type="text" id="novoProdutoImagem" v-model="novoProdutoImagem">
             </div>
             <button type="submit">Adicionar Produto</button>
         </form>
     </div>


    <div class="container" v-else-if="paginaAtual === 'pedidos' && usuarioLogado">
        <h1>Meus Pedidos</h1>
        <ul>
            <li v-for="(pedido, index) in pedidosRevendedor" :key="index">
                Pedido com {{ pedido.itens ? pedido.itens.length : 1 }} item(s) -
                <button @click="selecionarPedido(pedido)">Ver Detalhes</button>
            </li>
        </ul>
        <div v-if="produtoSelecionado" class="detalhes-pedido">
            <h2>Detalhes do Pedido</h2>
            <ul>
                <li v-for="item in pedidosRevendedor.find(p => p === produtoSelecionado)?.itens" :key="item.produtoId">
                    {{ item.nome }} - R$ {{ item.preco.toFixed(2) }}
                </li>
            </ul>
        </div>
    </div>

    <div class="container" v-else-if="paginaAtual === 'aprovacoes' && usuarioLogado && isAdmin">
        <h1>Aprovação de Pedidos</h1>
        <ul v-if="pedidosAprovacao.length > 0">
            <li v-for="pedido in pedidosAprovacao" :key="pedido.id">
                Pedido #{{ pedido.id }} de {{ pedido.revendedor }} ({{ pedido.itens.length }} itens) - Status: {{ pedido.status }}
                <button @click="aprovarPedido(pedido)" :disabled="pedido.status !== 'pendente'">Aprovar</button>
                <button @click="rejeitarPedido(pedido)" :disabled="pedido.status !== 'pendente'">Rejeitar</button>
                <button @click="selecionarPedido(pedido)">Ver Detalhes</button>
            </li>
        </ul>
        <p v-else>Não há pedidos pendentes para aprovação.</p>
        <div v-if="produtoSelecionado" class="detalhes-pedido">
            <h2>Detalhes do Pedido #{{ produtoSelecionado.id }}</h2>
            <p>Revendedor: {{ produtoSelecionado.revendedor }}</p>
            <p>Status: {{ produtoSelecionado.status }}</p>
            <h3>Itens:</h3>
            <ul>
                <li v-for="item in produtoSelecionado.itens" :key="item.nome">
                    {{ item.nome }} ({{ item.quantidade }})
                </li>
            </ul>
        </div>
    </div>

    <div class="container" v-else-if="usuarioLogado">
        <h1>{{ tituloPagina }}</h1>
        <p>{{ mensagem }}</p>
        <ul>
            <li v-for="(item, index) in lista" :key="index">{{ item }}</li>
        </ul>
        <div v-if="paginaAtual === 'sobre'">
            <h2>Nossa Missão</h2>
            <p>Oferecer soluções inovadoras para a gestão agrícola, impulsionando a produtividade e a sustentabilidade no campo.</p>
            <h2>Nossos Valores</h2>
            <ul>
                <li>Inovação</li>
                <li>Qualidade</li>
                <li>Sustentabilidade</li>
                <li>Parceria</li>
            </ul>
        </div>
        <div v-if="paginaAtual === 'contato'">
            <h3>Preencha o formulário abaixo para nos enviar uma mensagem:</h3>
            <form class="form-contato">
                <div class="form-group">
                    <label for="nomeContato">Nome:</label>
                    <input type="text" id="nomeContato" v-model="entradaTexto">
                </div>
                <div class="form-group">
                    <label for="emailContato">Email:</label>
                    <input type="email" id="emailContato" v-model="entradaTexto2">
                </div>
                <div class="form-group">
                    <label for="mensagemContato">Mensagem:</label>
                    <textarea id="mensagemContato" rows="5"></textarea>
                </div>
                <button type="submit">Enviar Mensagem</button>
            </form>
        </div>
    </div>
</template>