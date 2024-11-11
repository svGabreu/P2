from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Produto
from .forms import ProdutoForm
from django.shortcuts import render, get_object_or_404


def pagina_inicial(request):
    return render(request, 'produtos/pagina_inicial.html')

def listar_produtos(request):
    query = request.GET.get('q', '')  # Obtém o parâmetro de pesquisa da URL (caso exista)
    
    if query:
        produtos = Produto.objects.filter(nome__icontains=query)  # Filtra produtos pelo nome
    else:
        produtos = Produto.objects.all()  # Caso não haja filtro, retorna todos os produtos
    
    return render(request, 'produtos/listar.html', {'produtos': produtos, 'query': query})

def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()    
    return render(request, 'produtos/criar.html', {'form': form})

def deletar_produto(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    produto.delete()
    return redirect('listar_produtos')

def detalhes_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'produtos/detalhes_produto.html', {'produto': produto})

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')  # Redireciona para a página de listagem
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/editar_produto.html', {'form': form, 'produto': produto})