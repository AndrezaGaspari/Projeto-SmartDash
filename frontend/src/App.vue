<script setup>
import logoImg from '@/assets/Imagens/logo.png';
import tractorImg from '@/assets/Imagens/tractor.png';
import venenoImg from '@/assets/Imagens/veneno.png';
import veneno1Img from '@/assets/Imagens/veneno1.png';

import { ref, computed, watch, onMounted } from 'vue';

const usuarioLogado = ref(localStorage.getItem('usuarioLogado') === 'true' || false);
const userRole = ref(localStorage.getItem('userRole') || null);
const userId = ref(localStorage.getItem('userId') || null);
const estaNaPaginaInicial = ref(!usuarioLogado.value);
const mostrarLoginModal = ref(false);
const mostrarCadastroInicialModal = ref(false); // Nova modal para escolher o tipo de cadastro
const mostrarCadastroRevendedorModal = ref(false); // Modal de cadastro para revendedor
const mostrarCadastroLojaModal = ref(false); // Modal de cadastro para loja
const loginEmail = ref('');
const loginSenha = ref('');
const tipoLogin = ref('revendedor');
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
const revendedorIdLoja = ref(''); // Este campo pode não ser usado se a loja for dinâmica
const revendedorSenha = ref(''); // Novo campo senha para revendedor

// Campos do formulário de loja
const lojaCep = ref('');
const lojaCnpj = ref('');
const lojaNomeFantasia = ref('');
const lojaRazaoSocial = ref('');
const lojaTelefone = ref('');
const lojaEmail = ref('');
const lojaSenha = ref('');
const lojaEstado = ref('');
const lojaCidade = ref('');

const paginaAtual = ref(usuarioLogado.value ? 'produtos' : '');
const tituloPagina = ref('Produtos Agrícolas');
const mensagem = ref('Explore nossa variedade de produtos de alta qualidade para sua lavoura.');
const entradaTexto = ref('');
const entradaTexto2 = ref('');
const lista = ref([]);
const beneficios = ref(['Alta eficácia', 'Amplo espectro', 'Seguro para a cultura (se usado corretamente)']);
// Remova os produtos de teste iniciais se você planeja carregar do backend
const produtos = ref([]); // Inicialize como array vazio para carregar do backend
const filtroCategoria = ref('');
const filtroPrecoMin = ref(null);
const filtroPrecoMax = ref(null);
const filtroDisponibilidade = ref('');
const produtoSelecionado = ref(null);
const isAdmin = computed(() => userRole.value === 'loja');
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
// Nova ref para edição de quantidade (se você quiser editar a quantidade de um produto existente)
const edicaoQuantidade = ref(null);


// Novos campos para cadastro de produto
const novoProdutoNome = ref('');
const novoProdutoDescricao = ref('');
const novoProdutoCategoria = ref('');
const novoProdutoPreco = ref(null);
const novoProdutoDisponivel = ref(true);
const novoProdutoQuantidade = ref(null); // **NOVA REF PARA QUANTIDADE**
const novoProdutoVencimento = ref(''); // Para a data de vencimento
const novoProdutoFabricacao = ref(''); // Para a data de fabricação
const novoProdutoImagemFile = ref(null);      // Para armazenar o objeto File
const novoProdutoImagemPreview = ref(null);   // Para a URL de pré-visualização da imagem
const produtosFiltrados = computed(() => {
    return produtos.value.filter(produto => {
        const categoriaOk = !filtroCategoria.value || produto.categoria.toLowerCase().includes(filtroCategoria.value.toLowerCase());
        const precoMinOk = filtroPrecoMin.value === null || produto.preco >= filtroPrecoMin.value;
        const precoMaxOk = filtroPrecoMax.value === null || produto.preco <= filtroPrecoMax.value;
        const disponibilidadeOk = filtroDisponibilidade.value === '' || produto.disponivel.toString() === filtroDisponibilidade.value;
        return categoriaOk && precoMinOk && precoMaxOk && disponibilidadeOk;
    });
});

// Calcula se alguma modal de autenticação está visível
const estaNaPaginaDeAutenticacao = computed(() => {
    return mostrarLoginModal.value || mostrarCadastroInicialModal.value || mostrarCadastroRevendedorModal.value || mostrarCadastroLojaModal.value || estaNaPaginaInicial.value;
});

// Funções para exibir/ocultar modais
function mostrarLogin() {
    mostrarLoginModal.value = true;
    estaNaPaginaInicial.value = false;
    mostrarCadastroInicialModal.value = false;
    mostrarCadastroRevendedorModal.value = false;
    mostrarCadastroLojaModal.value = false;
}

function mostrarCadastroInicial() {
    mostrarCadastroInicialModal.value = true;
    estaNaPaginaInicial.value = false;
    mostrarLoginModal.value = false;
}

function mostrarCadastroRevendedor() {
    mostrarCadastroRevendedorModal.value = true;
    mostrarCadastroInicialModal.value = false;
}

function mostrarCadastroLoja() {
    mostrarCadastroLojaModal.value = true;
    mostrarCadastroInicialModal.value = false;
}


watch(usuarioLogado, (novoStatus) => {
    localStorage.setItem('usuarioLogado', novoStatus);
    estaNaPaginaInicial.value = !novoStatus;
    if (novoStatus) {
        mostrarLoginModal.value = false;
        mostrarCadastroInicialModal.value = false;
        mostrarCadastroRevendedorModal.value = false;
        mostrarCadastroLojaModal.value = false;

        if (userRole.value === 'loja') {
            paginaAtual.value = 'dashboard';
            fetchProdutos(); // Loja pode precisar carregar produtos ou outros dados
        } else if (userRole.value === 'revendedor') {
            paginaAtual.value = 'produtos';
            fetchProdutos(); // Revendedor deve carregar produtos
            fetchCarrinho(); // Revendedor deve carregar o carrinho
        } else {
            paginaAtual.value = 'produtos';
            fetchProdutos(); // Fallback
        }
    } else {
        paginaAtual.value = '';
        estaNaPaginaInicial.value = true;
    }
});

// **NOVA FUNÇÃO: FETCH PRODUTOS DO BACKEND**
async function fetchProdutos() {
    try {
        const response = await fetch('http://127.0.0.1:8000/produtos');
        if (!response.ok) {
            throw new Error('Erro ao carregar produtos do servidor.');
        }
        const data = await response.json();
        produtos.value = data; // Atualiza a ref 'produtos' com os dados do backend
        console.log("Produtos carregados do backend:", data);
    } catch (error) {
        console.error('Erro ao buscar produtos:', error);
        alert(`Erro ao carregar produtos: ${error.message}`);
    }
}

// **NOVA FUNÇÃO: FETCH CARRINHO DO BACKEND**
async function fetchCarrinho() {
    if (userRole.value === 'revendedor' && userId.value) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/carrinho/${userId.value}`); // Endpoint para obter carrinho do revendedor
            if (!response.ok) {
                // Se o carrinho estiver vazio ou não encontrado, o backend pode retornar 404
                // Nesse caso, inicializamos o carrinho local como vazio
                if (response.status === 404) {
                    pedidosRevendedor.value = [];
                    console.log("Carrinho vazio para este revendedor.");
                    return;
                }
                throw new Error('Erro ao carregar carrinho do servidor.');
            }
            const data = await response.json();
            pedidosRevendedor.value = data.itens || []; // Assumindo que a resposta tem uma chave 'itens'
            console.log("Carrinho carregado do backend:", data);
        } catch (error) {
            console.error('Erro ao buscar carrinho:', error);
            alert(`Erro ao carregar carrinho: ${error.message}`);
        }
    }
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
                fk_loja_id: Number(1) // ATENÇÃO: fk_loja_id está fixo em 1. Mantenha isso em mente.
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

    const payload = {
        nome_fantasia: lojaNomeFantasia.value,
        razao_social: lojaRazaoSocial.value,
        cnpj: lojaCnpj.value,
        senha: lojaSenha.value,
        estado: lojaEstado.value,
        cidade: lojaCidade.value,
        email: lojaEmail.value,
        cep: lojaCep.value,
        telefone: lojaTelefone.value,
    };

    console.log("Payload enviado:", payload);

    try {
        const response = await fetch("http://127.0.0.1:8000/lojas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Erro na resposta da API:", errorData);
            throw new Error(errorData.detail ? JSON.stringify(errorData.detail) : "Erro ao cadastrar loja");
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
        lojaEstado.value = '';
        lojaCidade.value = '';

        mostrarCadastroLojaModal.value = false;
        mostrarLoginModal.value = true;

    } catch (error) {
        alert(`Erro: ${error.message}`);
    }
}
// Função de login
async function loginRevendedor() {
    console.log("Tentando login de revendedor...");
    try {
        const response = await fetch('http://localhost:8000/login', { // Endpoint para revendedores
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
            alert(data.message || 'Login de revendedor bem-sucedido!');
            usuarioLogado.value = true;
            userRole.value = 'revendedor';
            userId.value = data.id;

            localStorage.setItem('usuarioLogado', 'true');
            localStorage.setItem('userRole', 'revendedor');
            localStorage.setItem('userId', data.id);

            // Chamada para carregar produtos e carrinho após login
            await fetchProdutos();
            await fetchCarrinho();

            paginaAtual.value = 'produtos';
            mostrarLoginModal.value = false;
        } else {
            alert(data.detail || 'Erro no login: credenciais inválidas ou erro do servidor.');
        }
    } catch (error) {
        console.error('Erro na requisição de login de revendedor:', error);
        alert('Erro ao conectar com o servidor para login de revendedor.');
    }
}

// NOVA FUNÇÃO: Login para Lojas
async function loginLoja() {
    console.log("Tentando login de loja...");
    try {
        const response = await fetch('http://localhost:8000/lojas/login', { // Endpoint para lojas
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
            alert(data.message || 'Login de loja bem-sucedido!');
            usuarioLogado.value = true;
            userRole.value = 'loja';
            userId.value = data.id;

            localStorage.setItem('usuarioLogado', 'true');
            localStorage.setItem('userRole', 'loja');
            localStorage.setItem('userId', data.id);

            // Chamada para carregar produtos após login
            await fetchProdutos(); // Lojas também podem ver produtos

            paginaAtual.value = 'dashboard';
            mostrarLoginModal.value = false;
        } else {
            alert(data.detail || 'Erro no login: credenciais inválidas ou erro do servidor.');
        }
    } catch (error) {
        console.error('Erro na requisição de login de loja:', error);
        alert('Erro ao conectar com o servidor para login de loja.');
    }
}

// Função para manipular o SUBMIT do formulário de login, chamando a função correta
function handleLoginSubmit() {
    if (tipoLogin.value === 'revendedor') {
        loginRevendedor();
    } else { // tipoLogin.value === 'loja'
        loginLoja();
    }
}
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        novoProdutoImagemFile.value = file;
        novoProdutoImagemPreview.value = URL.createObjectURL(file); // Cria URL para pré-visualização
    } else {
        novoProdutoImagemFile.value = null;
        novoProdutoImagemPreview.value = null;
    }
}

// Função para cadastrar produto 
// Função para cadastrar produto
async function cadastrarNovoProduto() {

    if (!novoProdutoNome.value || !novoProdutoCategoria.value || novoProdutoPreco.value === null || novoProdutoQuantidade.value === null) {
        alert('Por favor, preencha nome, categoria, preço e quantidade do produto.');
        return;
    }

    if (userRole.value !== 'loja' || !userId.value) {
        alert('Você precisa estar logado como loja para cadastrar produtos e o ID da loja deve estar disponível.');
        return;
    }
    const lojaId = parseInt(userId.value);
    if (isNaN(lojaId)) {
        alert('Erro: ID da loja inválido para cadastro de produto. Por favor, faça login novamente.');
        console.error('userId.value não é um número válido para loja:', userId.value);
        return;
    }

    // *** MUDANÇA AQUI: Usar FormData para enviar dados mistos (texto + arquivo) ***
    const formData = new FormData();
    formData.append('nome', novoProdutoNome.value);
    formData.append('descricao', novoProdutoDescricao.value);
    formData.append('categoria', novoProdutoCategoria.value);
    formData.append('valor_produto', parseFloat(novoProdutoPreco.value));
    formData.append('quantidade', parseInt(novoProdutoQuantidade.value));
    formData.append('fk_loja_id', lojaId); // fk_loja_id enviado

    // Adicione campos opcionais apenas se tiverem valor
    if (novoProdutoVencimento.value) {
        formData.append('vencimento', novoProdutoVencimento.value);
    }
    if (novoProdutoFabricacao.value) {
        formData.append('fabricacao', novoProdutoFabricacao.value);
    }
    if (novoProdutoImagemFile.value) {
        formData.append('imagem', novoProdutoImagemFile.value); // Anexa o OBJETO FILE aqui
    }
    // Adicione o campo 'disponivel'. FormData trata booleanos automaticamente.
    formData.append('disponivel', novoProdutoDisponivel.value);


    try {
        const response = await fetch('http://127.0.0.1:8000/produtos/', { // Endpoint POST do seu FastAPI
            method: 'POST',
            // *** MUDANÇA AQUI: REMOVA O CABEÇALHO 'Content-Type' MANUALMENTE ***
            // O navegador definirá automaticamente o Content-Type: multipart/form-data com a boundary correta
            // headers: { 'Content-Type': 'application/json' }, // <-- REMOVA OU COMENTE ESTA LINHA!
            body: formData, // *** MUDANÇA AQUI: Envie o objeto FormData ***
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Erro detalhado do backend ao cadastrar produto:", errorData);
            throw new Error(errorData.detail ? JSON.stringify(errorData.detail) : 'Erro ao cadastrar produto no servidor.');
        }

        const produtoCriado = await response.json();
        alert('Produto cadastrado com sucesso!');
        console.log("Produto criado no backend:", produtoCriado);

        await fetchProdutos();

        // Limpa os campos do formulário
        novoProdutoNome.value = '';
        novoProdutoDescricao.value = '';
        novoProdutoCategoria.value = '';
        novoProdutoPreco.value = null;
        novoProdutoQuantidade.value = null;
        novoProdutoVencimento.value = '';
        novoProdutoFabricacao.value = '';
        novoProdutoDisponivel.value = true;
        novoProdutoImagemFile.value = null;     // Limpa o arquivo selecionado
        novoProdutoImagemPreview.value = null;  // Limpa a pré-visualização

        navegarPara('produtos'); // Volta para a lista de produtos após o cadastro
    } catch (error) {
        console.error('Erro ao cadastrar produto:', error);
        alert(`Erro ao cadastrar produto: ${error.message}`);
    }
}

function logout() {
    usuarioLogado.value = false;
    userRole.value = null;
    userId.value = null;
    localStorage.removeItem('usuarioLogado');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userId');
    paginaAtual.value = '';
    estaNaPaginaInicial.value = true;
    produtos.value = []; // Limpa os produtos do frontend ao deslogar
    pedidosRevendedor.value = []; // Limpa o carrinho do frontend ao deslogar
}

function navegarPara(pagina) {
    if (usuarioLogado.value || pagina === '') {
        paginaAtual.value = pagina;
        produtoSelecionado.value = null;
        mostrarLoginModal.value = false;
        mostrarCadastroInicialModal.value = false;
        mostrarCadastroRevendedorModal.value = false;
        mostrarCadastroLojaModal.value = false;

        if (pagina === 'produtos' || pagina === 'dashboard') {
            fetchProdutos();
            // Se for revendedor, também carregar o carrinho
            if (userRole.value === 'revendedor') {
                fetchCarrinho();
            }
        }
    }
}
async function adicionarAoPedido(produto) {
    console.log("DEBUG: userRole.value =", userRole.value);
    console.log("DEBUG: userId.value =", userId.value);

    if (userRole.value !== 'revendedor' || !userId.value) {
        alert('Você precisa estar logado como revendedor para adicionar itens ao pedido.');
        return;
    }

    const revendedorId = parseInt(userId.value);
    if (isNaN(revendedorId)) {
        alert('Erro: ID do revendedor inválido. Por favor, faça login novamente.');
        console.error('userId.value não é um número válido:', userId.value);
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/carrinho/', { // Endpoint para adicionar item ao carrinho
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                revendedor_id: revendedorId,
                produto_id: produto.id,
                quantidade: 1, // Assumindo quantidade 1 ao adicionar
                nome_produto: produto.nome,
                preco_unitario: produto.preco // Ou produto.valor_produto, dependendo do que vem do backend
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Erro detalhado do FastAPI (adicionar ao pedido):", errorData);
            throw new Error(errorData.detail ? JSON.stringify(errorData.detail) : "Erro ao adicionar produto ao pedido.");
        }

        const data = await response.json();
        alert(`${produto.nome} adicionado ao pedido.`);
        console.log("Produto adicionado ao pedido:", data);
        await fetchCarrinho(); // ATUALIZA O CARRINHO NO FRONTEND
    } catch (error) {
        console.error('Erro ao adicionar ao pedido:', error);
        alert(`Erro ao adicionar ao pedido: ${error.message || error}`);
    }
}

async function enviarPedido() {
    if (pedidosRevendedor.value.length === 0) {
        alert('Seu pedido está vazio.');
        return;
    }

    if (userRole.value !== 'revendedor' || !userId.value) {
        alert('Você precisa estar logado como revendedor para enviar um pedido.');
        return;
    }

    const revendedorId = parseInt(userId.value);
    if (isNaN(revendedorId)) {
        alert('Erro: ID do revendedor inválido. Por favor, faça login novamente.');
        return;
    }

    try {
        console.log(`Enviando pedido (limpando carrinho) para revendedor_id: ${revendedorId}`);

        const pedidoData = {
            revendedor_id: revendedorId,
            itens: pedidosRevendedor.value.map(item => ({
                produto_id: item.produto_id,
                quantidade: item.quantidade,
                preco_unitario: item.preco_unitario // Ou `item.preco` se o backend o chama assim
            }))
        };

        const responseEnviarPedido = await fetch('http://127.0.0.1:8000/pedidos', { // Exemplo de endpoint para enviar pedido
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pedidoData),
        });

        if (!responseEnviarPedido.ok) {
            const errorData = await responseEnviarPedido.json();
            throw new Error(errorData.detail ? JSON.stringify(errorData.detail) : "Erro ao enviar o pedido para aprovação.");
        }

        // 2. Após o envio bem-sucedido, limpar o carrinho no backend (se houver um endpoint para isso)
        // Isso é opcional, dependendo de como seu backend gerencia o "envio" vs "limpeza".
        // Se o endpoint `/pedidos` já limpa o carrinho no backend, você não precisa desta segunda chamada.
        // Mas se precisa de uma chamada separada para limpar o carrinho:
        const responseLimparCarrinho = await fetch(`http://127.0.0.1:8000/carrinho/${revendedorId}`, {
            method: "DELETE", // Endpoint para limpar todo o carrinho de um revendedor
            headers: { 'Content-Type': 'application/json' },
        });

        if (!responseLimparCarrinho.ok) {
            console.warn("Aviso: Pedido enviado, mas houve um erro ao limpar o carrinho no backend.", await responseLimparCarrinho.json());
        }


        alert('Pedido enviado para aprovação!');
        pedidosRevendedor.value = []; // Limpa o frontend após sucesso
        navegarPara('pedidos'); // Opcional: mantém na página de pedidos que agora estará vazia
    } catch (error) {
        console.error('Erro ao enviar pedido:', error);
        alert(`Erro ao enviar pedido: ${error.message}`);
    }
}
async function removerItemDoPedido(produtoId) {
    if (userRole.value !== 'revendedor' || !userId.value) {
        alert('Você precisa estar logado como revendedor para remover itens do pedido.');
        return;
    }

    if (!confirm('Tem certeza que deseja remover este item do seu pedido?')) {
        return;
    }

    const revendedorId = parseInt(userId.value);
    if (isNaN(revendedorId)) {
        alert('Erro: ID do revendedor inválido. Por favor, faça login novamente.');
        return;
    }

    try {
        console.log(`Removendo produto ${produtoId} do carrinho do revendedor ${revendedorId}`);
        // **CORREÇÃO DA URL DO ENDPOINT DELETE**
        const response = await fetch(`http://127.0.0.1:8000/carrinho/${revendedorId}/item/${produtoId}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Erro detalhado do FastAPI (remover item do pedido):", errorData);
            throw new Error(errorData.detail ? JSON.stringify(errorData.detail) : "Erro ao remover item do carrinho.");
        }

        alert('Item removido com sucesso!');
        await fetchCarrinho(); // Atualiza a lista do carrinho após remover
    } catch (error) {
        console.error('Erro ao remover item:', error);
        alert(`Erro ao remover item: ${error.message}`);
    }
}
function selecionarProduto(produto) {
    produtoSelecionado.value = produto;
}

function aprovarPedido(pedidoId) {
    const pedido = pedidosAprovacao.value.find(p => p.id === pedidoId);
    if (pedido) {
        alert(`Pedido ${pedido.id} aprovado.`);
        pedido.status = 'aprovado';
        pedidosAprovacao.value = pedidosAprovacao.value.filter(p => p.id !== pedidoId);
    }
}

function rejeitarPedido(pedidoId) {
    const pedido = pedidosAprovacao.value.find(p => p.id === pedidoId);
    if (pedido) {
        alert(`Pedido ${pedido.id} rejeitado.`);
        pedido.status = 'rejeitado';
        pedidosAprovacao.value = pedidosAprovacao.value.filter(p => p.id !== pedidoId);
    }
}

// FUNÇÃO EDITAR PRODUTO ATUALIZADA
function iniciarEdicaoProduto(produto) {
    produtoEditando.value = produto;
    edicaoNome.value = produto.nome;
    edicaoPreco.value = produto.valor_produto; // **USAR valor_produto, não preco**
    edicaoDescricao.value = produto.descricao;
    edicaoCategoria.value = produto.categoria;
    edicaoDisponivel.value = produto.disponivel;
    edicaoImagem.value = produto.imagem;
    edicaoQuantidade.value = produto.quantidade; // **NOVO: Carrega quantidade para edição**
}

// FUNÇÃO SALVAR EDIÇÃO PRODUTO ATUALIZADA - AGORA FAZ CHAMADA AO BACKEND
async function salvarEdicaoProduto() {
    if (!produtoEditando.value) {
        return;
    }

    // Validação para fk_loja_id: Apenas lojas podem editar produtos.
    if (userRole.value !== 'loja' || !userId.value) {
        alert('Você precisa estar logado como loja para editar produtos.');
        cancelarEdicaoProduto(); // Cancela a edição
        return;
    }
    const lojaId = parseInt(userId.value);
    if (isNaN(lojaId)) {
        alert('Erro: ID da loja inválido para edição de produto. Faça login novamente.');
        cancelarEdicaoProduto();
        return;
    }

    const produtoId = produtoEditando.value.id;

    // Prepare os dados para enviar ao backend para atualização
    const produtoAtualizado = {
        nome: edicaoNome.value,
        descricao: edicaoDescricao.value,
        categoria: edicaoCategoria.value,
        valor_produto: parseFloat(edicaoPreco.value), // **AQUI: Mapeado de 'preco' para 'valor_produto'**
        quantidade: parseInt(edicaoQuantidade.value), // **AQUI: Incluído quantidade**
        vencimento: produtoEditando.value.vencimento, // Mantenha, se não houver campos de edição para ele
        fabricacao: produtoEditando.value.fabricacao, // Mantenha, se não houver campos de edição para ele
        fk_loja_id: lojaId, // Enviando o ID da loja logada
        imagem: edicaoImagem.value || '',
        disponivel: edicaoDisponivel.value,
    };

    try {
        const response = await fetch(`http://127.0.0.1:8000/produtos/${produtoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(produtoAtualizado),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Erro detalhado do backend ao salvar edição:", errorData);
            throw new Error(errorData.detail ? JSON.stringify(errorData.detail) : 'Erro ao atualizar produto no servidor.');
        }

        const data = await response.json();
        alert('Produto atualizado com sucesso!');
        console.log("Produto atualizado no backend:", data);

        // Atualiza a lista local de produtos após o sucesso da API
        await fetchProdutos(); // A melhor forma de garantir a sincronização

        produtoEditando.value = null; // Fecha o modal de edição
    } catch (error) {
        console.error('Erro ao salvar edição do produto:', error);
        alert(`Erro ao salvar edição: ${error.message}`);
    }
}

function cancelarEdicaoProduto() {
    produtoEditando.value = null;
}

// **NOVA FUNÇÃO: DELETAR PRODUTO (Faz chamada ao Backend)**
async function deletarProduto(produtoId) {
    if (!confirm('Tem certeza que deseja deletar este produto? Esta ação é irreversível.')) {
        return;
    }

    // Validação de permissão
    if (userRole.value !== 'loja' || !userId.value) {
        alert('Você precisa estar logado como loja para deletar produtos.');
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/produtos/${produtoId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Erro detalhado do backend ao deletar produto:", errorData);
            throw new Error(errorData.detail ? JSON.stringify(errorData.detail) : 'Erro ao deletar produto no servidor.');
        }

        alert('Produto deletado com sucesso!');
        console.log(`Produto ${produtoId} deletado.`);
        await fetchProdutos(); // Atualiza a lista de produtos no frontend
    } catch (error) {
        console.error('Erro ao deletar produto:', error);
        alert(`Erro ao deletar produto: ${error.message}`);
    }
}


onMounted(() => {
    // Redireciona para a página correta ao carregar, se já estiver logado
    if (usuarioLogado.value) {
        if (userRole.value === 'loja') {
            paginaAtual.value = 'dashboard';
        } else if (userRole.value === 'revendedor') {
            paginaAtual.value = 'produtos';
        } else {
            paginaAtual.value = 'produtos'; // Fallback
        }
        estaNaPaginaInicial.value = false;
        fetchProdutos(); // Carrega produtos quando a página é montada e o usuário está logado
        if (userRole.value === 'revendedor') {
            fetchCarrinho(); // Carrega o carrinho para revendedores
        }
    } else {
        estaNaPaginaInicial.value = true;
    }
});
</script>

<template>
  <div id="app-container">
    <header class="app-header">
      <div class="logo-container">
        <img :src="logoImg" alt="Logo da Loja Agrícola" class="logo-img" />
        <span class="app-title">SmartDash</span>
      </div>
      <nav v-if="usuarioLogado" class="main-nav">
        <ul>
          <li>
            <a href="#" @click.prevent="navegarPara('produtos')"
              >Catálogo de Produtos</a
            >
          </li>
          <li v-if="userRole === 'revendedor'">
            <a href="#" @click.prevent="navegarPara('pedidos')"
              >Meus Pedidos</a
            >
          </li>
          <li v-if="isAdmin">
            <a href="#" @click.prevent="navegarPara('dashboard')">Dashboard</a>
          </li>
          <li v-if="isAdmin">
            <a href="#" @click.prevent="navegarPara('cadastro-produto')"
              >Cadastrar Produto</a
            >
          </li>
          <li v-if="isAdmin">
            <a href="#" @click.prevent="navegarPara('aprovacoes')"
              >Aprovações</a
            >
          </li>
          <li v-if="isAdmin">
            <a href="#" @click.prevent="navegarPara('vendas')"
              >Relatórios de Vendas</a
            >
          </li>
          <li>
            <a href="#" @click.prevent="navegarPara('sobre')">Sobre Nós</a>
          </li>
          <li>
            <a href="#" @click.prevent="navegarPara('contato')">Contato</a>
          </li>
        </ul>
      </nav>
      <div class="auth-controls">
        <button v-if="usuarioLogado" @click="logout" class="logout-button">
          Sair
        </button>
        <div v-else class="auth-buttons">
          <button @click="mostrarLogin" class="login-button">Login</button>
          <button @click="mostrarCadastroInicial" class="register-button">
            Cadastrar
          </button>
        </div>
      </div>
    </header>

    <main
      :class="{ 'auth-page-main': !usuarioLogado, 'logged-in-main': usuarioLogado }"
    >
      <section v-if="estaNaPaginaInicial && !usuarioLogado" class="pagina-inicial">
        <h1>Bem-vindo à Smartdash!</h1>
        <p>Conecte-se para explorar nosso catálogo de produtos e fazer seus pedidos.</p>
        <div class="auth-buttons">
          <button @click="mostrarLogin" class="login-button">Login</button>
          <button @click="mostrarCadastroInicial" class="register-button">
            Cadastrar
          </button>
        </div>
        <img :src="tractorImg" alt="Trator no Campo" class="initial-page-image" />
      </section>

      <div
        v-if="
          mostrarLoginModal ||
          mostrarCadastroInicialModal ||
          mostrarCadastroRevendedorModal ||
          mostrarCadastroLojaModal ||
          produtoEditando
        "
        class="modal-overlay"
      >
        <div v-if="mostrarLoginModal" class="modal-content login-container">
          <h2>Login</h2>
          <form @submit.prevent="handleLoginSubmit">
            <div class="form-group">
              <label for="loginTipo">Entrar como:</label>
              <select id="loginTipo" v-model="tipoLogin">
                <option value="revendedor">Revendedor</option>
                <option value="loja">Loja</option>
              </select>
            </div>
            <div class="form-group">
              <label for="loginEmail">Email:</label>
              <input type="email" id="loginEmail" v-model="loginEmail" required />
            </div>
            <div class="form-group">
              <label for="loginSenha">Senha:</label>
              <input type="password" id="loginSenha" v-model="loginSenha" required />
            </div>
            <button type="submit">Entrar</button>
          </form>
          <p class="link-cadastro">
            Não tem conta?
            <a href="#" @click.prevent="mostrarCadastroInicial">Cadastre-se</a>
          </p>
          <button @click="mostrarLoginModal = false" class="close-modal-button">
            X
          </button>
        </div>

        <div
          v-if="mostrarCadastroInicialModal"
          class="modal-content cadastro-inicial-container"
        >
          <h2>Selecione o tipo de cadastro</h2>
          <div class="cadastro-options">
            <button @click="mostrarCadastroRevendedor">Sou Revendedor</button>
            <button @click="mostrarCadastroLoja">Sou Loja</button>
          </div>
          <p class="link-login">
            Já tem conta? <a href="#" @click.prevent="mostrarLogin">Login</a>
          </p>
          <button
            @click="mostrarCadastroInicialModal = false"
            class="close-modal-button"
          >
            X
          </button>
        </div>

        <div
          v-if="mostrarCadastroRevendedorModal"
          class="modal-content cadastro-revendedor-container"
        >
          <h2>Cadastro de Revendedor</h2>
          <form @submit.prevent="cadastrarRevendedor">
            <div class="form-group">
              <label for="revendedorNome">Nome Completo:</label>
              <input type="text" id="revendedorNome" v-model="revendedorNome" required />
            </div>
            <div class="form-group">
              <label for="revendedorEmail">Email:</label>
              <input type="email" id="revendedorEmail" v-model="revendedorEmail" required />
            </div>
            <div class="form-group">
              <label for="revendedorSenha">Senha:</label>
              <input type="password" id="revendedorSenha" v-model="revendedorSenha" required />
            </div>
            <div class="form-group">
              <label for="revendedorCpf">CPF:</label>
              <input type="text" id="revendedorCpf" v-model="revendedorCpf" required />
            </div>
            <div class="form-group">
              <label for="revendedorTelefoneCelular">Telefone Celular:</label>
              <input type="tel" id="revendedorTelefoneCelular" v-model="revendedorTelefoneCelular" />
            </div>
            <div class="form-group">
              <label for="revendedorDataNascimento">Data de Nascimento:</label>
              <input type="date" id="revendedorDataNascimento" v-model="revendedorDataNascimento" />
            </div>
            <div class="form-group">
              <label for="revendedorCep">CEP:</label>
              <input type="text" id="revendedorCep" v-model="revendedorCep" />
            </div>
            <div class="form-group">
              <label for="revendedorRua">Rua:</label>
              <input type="text" id="revendedorRua" v-model="revendedorRua" />
            </div>
            <div class="form-group">
              <label for="revendedorNumeroCasa">Número:</label>
              <input type="number" id="revendedorNumeroCasa" v-model="revendedorNumeroCasa" />
            </div>
            <div class="form-group">
              <label for="revendedorComplemento">Complemento:</label>
              <input type="text" id="revendedorComplemento" v-model="revendedorComplemento" />
            </div>
            <div class="form-group">
              <label for="revendedorBairro">Bairro:</label>
              <input type="text" id="revendedorBairro" v-model="revendedorBairro" />
            </div>
            <div class="form-group">
              <label for="revendedorCidade">Cidade:</label>
              <input type="text" id="revendedorCidade" v-model="revendedorCidade" required />
            </div>
            <div class="form-group">
              <label for="revendedorEstado">Estado (UF):</label>
              <input
                type="text"
                id="revendedorEstado"
                v-model="revendedorEstado"
                maxlength="2"
                required
              />
            </div>
            <button type="submit">Cadastrar Revendedor</button>
          </form>
          <button @click="mostrarCadastroInicial" class="close-modal-button">
            X
          </button>
        </div>

        <div
          v-if="mostrarCadastroLojaModal"
          class="modal-content cadastro-loja-container"
        >
          <h2>Cadastro de Loja</h2>
          <form @submit.prevent="cadastrarLoja">
            <div class="form-group">
              <label for="lojaCnpj">CNPJ:</label>
              <input type="text" id="lojaCnpj" v-model="lojaCnpj" required />
            </div>
            <div class="form-group">
              <label for="lojaNomeFantasia">Nome Fantasia:</label>
              <input type="text" id="lojaNomeFantasia" v-model="lojaNomeFantasia" required />
            </div>
            <div class="form-group">
              <label for="lojaRazaoSocial">Razão Social:</label>
              <input type="text" id="lojaRazaoSocial" v-model="lojaRazaoSocial" required />
            </div>
            <div class="form-group">
              <label for="lojaEmail">Email:</label>
              <input type="email" id="lojaEmail" v-model="lojaEmail" required />
            </div>
            <div class="form-group">
              <label for="lojaSenha">Senha:</label>
              <input type="password" id="lojaSenha" v-model="lojaSenha" required />
            </div>
            <div class="form-group">
              <label for="lojaTelefone">Telefone:</label>
              <input type="tel" id="lojaTelefone" v-model="lojaTelefone" />
            </div>
            <div class="form-group">
              <label for="estadoLoja">Estado:</label>
              <input type="text" id="estadoLoja" v-model="lojaEstado" required />
            </div>
            <div class="form-group">
              <label for="cidadeLoja">Cidade:</label>
              <input type="text" id="cidadeLoja" v-model="lojaCidade" required />
            </div>
            <div class="form-group">
              <label for="lojaCep">CEP:</label>
              <input type="text" id="lojaCep" v-model="lojaCep" />
            </div>
            <button type="submit">Cadastrar Loja</button>
          </form>
          <button @click="mostrarCadastroInicial" class="close-modal-button">
            X
          </button>
        </div>

        <div v-if="produtoEditando && isAdmin" class="modal-content modal-edit-product">
          <h2>Editar Produto: {{ produtoEditando.nome }}</h2>
          <form @submit.prevent="salvarEdicaoProduto">
            <div class="form-group">
              <label for="edicaoNome">Nome:</label>
              <input type="text" id="edicaoNome" v-model="edicaoNome" placeholder="Nome" />
            </div>
            <div class="form-group">
              <label for="edicaoPreco">Preço:</label>
              <input
                type="number"
                id="edicaoPreco"
                v-model="edicaoPreco"
                placeholder="Preço"
                step="0.01"
              />
            </div>
            <div class="form-group">
              <label for="edicaoDescricao">Descrição:</label>
              <textarea
                id="edicaoDescricao"
                v-model="edicaoDescricao"
                placeholder="Descrição"
              ></textarea>
            </div>
            <div class="form-group">
              <label for="edicaoCategoria">Categoria:</label>
              <input
                type="text"
                id="edicaoCategoria"
                v-model="edicaoCategoria"
                placeholder="Categoria"
              />
            </div>
            <div class="form-group checkbox-group">
              <label for="edicaoDisponivel">Disponível:</label>
              <input type="checkbox" id="edicaoDisponivel" v-model="edicaoDisponivel" />
            </div>
            <div class="form-group">
              <label for="edicaoImagem">URL da Imagem:</label>
              <input
                type="text"
                id="edicaoImagem"
                v-model="edicaoImagem"
                placeholder="URL da Imagem"
              />
            </div>
            <div class="button-group">
              <button type="submit">Salvar Alterações</button>
              <button type="button" @click="cancelarEdicaoProduto">Cancelar</button>
            </div>
          </form>
          <button @click="cancelarEdicaoProduto" class="close-modal-button">
            X
          </button>
        </div>
      </div>

      <div v-if="usuarioLogado" class="site-content">
        <h1>{{ tituloPagina }}</h1>
        <p>{{ mensagem }}</p>

        <section v-if="paginaAtual === 'produtos'" class="product-catalog-section">
          <div class="filters">
            <div class="form-group">
              <label for="filterCategory">Categoria:</label>
              <input
                type="text"
                id="filterCategory"
                v-model="filtroCategoria"
                placeholder="Filtrar por Categoria"
              />
            </div>

            <div class="form-group">
              <label for="filterMinPrice">Preço Mín.:</label>
              <input
                type="number"
                id="filterMinPrice"
                v-model="filtroPrecoMin"
                placeholder="Preço Mín."
                step="0.01"
              />
            </div>

            <div class="form-group">
              <label for="filterMaxPrice">Preço Máx.:</label>
              <input
                type="number"
                id="filterMaxPrice"
                v-model="filtroPrecoMax"
                placeholder="Preço Máx."
                step="0.01"
              />
            </div>

            <div class="form-group">
              <label for="filterAvailability">Disponibilidade:</label>
              <select id="filterAvailability" v-model="filtroDisponibilidade">
                <option value="">Todos</option>
                <option value="true">Disponível</option>
                <option value="false">Indisponível</option>
              </select>
            </div>
          </div>

          <div class="product-grid">
            <article v-for="produto in produtosFiltrados" :key="produto.id" class="product-card">
              <img :src="produto.imagem" :alt="produto.nome" />
              <h3>{{ produto.nome }}</h3>
              <p class="product-description">{{ produto.descricao }}</p>
              <p class="product-price">R$ {{ produto.valor_produto.toFixed(2)  }}</p>
              <p :class="{ disponivel: produto.disponivel, indisponivel: !produto.disponivel }">
                {{ produto.disponivel ? "Disponível" : "Indisponível" }}
              </p>
              <div class="product-actions">
                <button
                  v-if="userRole === 'revendedor' && produto.disponivel"
                  @click="adicionarAoPedido(produto)"
                >
                  Adicionar ao Pedido
                </button>
                <div v-if="isAdmin">
                  <button @click="iniciarEdicaoProduto(produto)">Editar</button>
                  <button @click="deletarProduto(produto.id)">Excluir</button>
                </div>
              </div>
            </article>
          </div>
        </section>

        <section v-else-if="paginaAtual === 'pedidos' && userRole === 'revendedor'" class="my-orders-section container">
          <h2>Meus Pedidos</h2>
          <ul v-if="pedidosRevendedor.length">
            <li v-for="pedido in pedidosRevendedor" :key="pedido.id" class="order-item">
              <div class="order-header">
                <span>Pedido ID: {{ pedido.id }}</span>
                <span :class="['order-status', pedido.status]">{{ pedido.status }}</span>
              </div>
              <ul class="order-items-list">
                <li v-for="(item, index) in pedido.itens" :key="index">
                  {{ item.nome }} (Quantidade: {{ item.quantidade }})
                </li>
              </ul>
            </li>
          </ul>
          <p v-else class="empty-state">Você não possui pedidos realizados ainda.</p>
          <button
            v-if="pedidosRevendedor.length > 0 && pedidosRevendedor.some((p) => p.status === 'pendente')"
            @click="enviarPedido"
            class="submit-order-button"
          >
            Enviar Pedido
          </button>
        </section>

        <section v-else-if="paginaAtual === 'aprovacoes' && isAdmin" class="approvals-section container">
          <h2>Aprovação de Pedidos</h2>
          <ul v-if="pedidosAprovacao.length" class="approval-list">
            <li v-for="pedido in pedidosAprovacao" :key="pedido.id" class="approval-item">
              <div class="approval-header">
                <span>Pedido ID: {{ pedido.id }} de {{ pedido.revendedor }}</span>
                <span :class="['order-status', pedido.status]">{{ pedido.status }}</span>
              </div>
              <ul class="approval-items-list">
                <li v-for="(item, index) in pedido.itens" :key="index">
                  {{ item.nome }} (Quantidade: {{ item.quantidade }})
                </li>
              </ul>
              <div class="approval-actions">
                <button @click="aprovarPedido(pedido.id)" class="approve-button">
                  Aprovar
                </button>
                <button @click="rejeitarPedido(pedido.id)" class="reject-button">
                  Rejeitar
                </button>
              </div>
            </li>
          </ul>
          <p v-else class="empty-state">Não há pedidos pendentes de aprovação.</p>
        </section>

        <section v-else-if="paginaAtual === 'dashboard' && isAdmin" class="dashboard-section container">
          <h2>Dashboard de Vendas</h2>
          <p>Gráficos e métricas de desempenho aqui.</p>
          <div class="metricas">
            <div>
              <h3>Vendas Totais Mês</h3>
              <p>R$ 15.450,00</p>
            </div>
            <div>
              <h3>Pedidos Aprovados</h3>
              <p>25</p>
            </div>
            <div>
              <h3>Produtos em Estoque</h3>
              <p>120</p>
            </div>
          </div>
        </section>
<section v-else-if="paginaAtual === 'cadastro-produto' && isAdmin" class="add-product-section container">
  <h2>Cadastrar Novo Produto</h2>
  <form @submit.prevent="cadastrarNovoProduto" class="form-cadastro-produto">
    <div class="form-group">
      <label for="novoNome">Nome:</label>
      <input type="text" id="novoNome" v-model="novoProdutoNome" required />
    </div>
<div class="form-group">
  <label for="novoDescricao">Descrição:</label>
  <textarea id="novoDescricao" v-model="novoProdutoDescricao" required></textarea>
</div>
    <div class="form-group">
      <label for="novoCategoria">Categoria:</label>
      <input type="text" id="novoCategoria" v-model="novoProdutoCategoria" required />
    </div>
    <div class="form-group">
      <label for="novoQuantidade">Quantidade:</label>
      <input
        type="number"
        id="novoQuantidade"
        v-model="novoProdutoQuantidade"
        required
      />
    </div>

    <div class="form-group">
      <label for="novoVencimento">Data de Vencimento:</label>
      <input type="date" id="novoVencimento" v-model="novoProdutoVencimento" />
    </div>
    <div class="form-group">
      <label for="novoFabricacao">Data de Fabricação:</label>
      <input type="date" id="novoFabricacao" v-model="novoProdutoFabricacao" />
    </div>
    <div class="form-group">
      <label for="novoPreco">Preço:</label>
      <input
        type="number"
        id="novoPreco"
        v-model="novoProdutoPreco"
        step="0.01"
        required
      />
    </div>
    <div class="form-group checkbox-group">
      <label for="novoDisponivel">Disponível:</label>
      <input type="checkbox" id="novoDisponivel" v-model="novoProdutoDisponivel" />
    </div>
  <div class="form-group">
  <label for="novoImagem">URL da Imagem:</label> <input
    type="file"
    id="novoImagem"
    @change="handleImageUpload"
    accept="image/*" />
  <img v-if="novoProdutoImagemPreview" :src="novoProdutoImagemPreview" alt="Pré-visualização da imagem" style="max-width: 100px; max-height: 100px; margin-top: 10px;" />
</div>
    <button type="submit">Adicionar Produto</button>
  </form>
</section>

        <section v-else-if="paginaAtual === 'vendas' && isAdmin" class="sales-report-section container">
          <h2>Relatórios de Vendas</h2>
          <p>Aqui você pode ver os relatórios detalhados de vendas.</p>
          <ul v-if="lista && lista.length">
            <li v-for="(item, index) in lista" :key="index">{{ item }}</li>
          </ul>
          <p v-else>Nenhum relatório de vendas disponível no momento.</p>
        </section>

        <section v-else-if="paginaAtual === 'sobre'" class="about-us-section container">
          <h2>Sobre a Nossa Empresa</h2>
          <p>
            Nossa missão é fornecer os melhores produtos agrícolas para garantir a
            produtividade e sustentabilidade do campo.
          </p>
          <p>
            Desde 2023, trabalhamos com paixão para conectar produtores e revendedores,
            impulsionando a agricultura brasileira.
          </p>
          <img :src="veneno1Img" alt="Imagem Ilustrativa" class="about-us-image" />
        </section>

        <section v-else-if="paginaAtual === 'contato'" class="contact-section container">
          <h2>Entre em Contato Conosco</h2>
          <p>Estamos prontos para atendê-lo!</p>
          <p>Email: contato@lojaagricola.com.br</p>
          <p>Telefone: (XX) XXXX-XXXX</p>
          <address>
            Endereço: Rua do Campo, 123 - Zona Rural, Cidade Agrícola - SP
          </address>
          <img :src="venenoImg" alt="Imagem Ilustrativa" class="contact-image" />
        </section>
      </div>
    </main>

    <footer class="app-footer">
      <p>&copy; 2025 Loja SmartDash. Todos os direitos reservados.</p>
      <p>
        Desenvolvido por Andreza Gaspari, Ana Luiza Quintana, Vitor Hugo Oliveira,Fernanda
        & Gustavo Grotto
      </p>
    </footer>
  </div>
</template>

<style>
/* Importe seu main.css aqui */
@import "./assets/main.css";
</style>