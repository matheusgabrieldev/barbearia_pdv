from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required

from .models import Cliente, Servico, Agendamento
from .forms import ClienteForm, ServicoForm, AgendamentoForm, UserRegistrationForm


# 🔐 LOGIN
def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            error = 'Usuário ou senha inválidos'

    return render(request, 'pdv/login.html', {'error': error})


# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# 📝 REGISTRO
def register_view(request):
    form = UserRegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')

    return render(request, 'pdv/register.html', {'form': form})


# 📊 DASHBOARD
@login_required
def dashboard(request):
    agendamentos = Agendamento.objects.all()
    total_vendas = sum(a.servico.preco for a in agendamentos)

    return render(request, 'pdv/dashboard.html', {
        'agendamentos': agendamentos,
        'total_vendas': total_vendas
    })


# 👥 LISTAR CLIENTES
@login_required
def clientes_view(request):
    clientes = Cliente.objects.all()
    return render(request, 'pdv/clientes.html', {'clientes': clientes})


# ➕ CRIAR CLIENTE
@login_required
def criar_cliente(request):
    form = ClienteForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('clientes')

    return render(request, 'pdv/criar_cliente.html', {'form': form})


# 🛠️ LISTAR SERVIÇOS
@login_required
def servicos_view(request):
    servicos = Servico.objects.all()
    return render(request, 'pdv/servicos.html', {'servicos': servicos})


# ➕ CRIAR SERVIÇO
@login_required
def criar_servico(request):
    form = ServicoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('servicos')

    return render(request, 'pdv/criar_servico.html', {'form': form})


# 📅 LISTAR AGENDAMENTOS
@login_required
def agendamentos_view(request):
    agendamentos = Agendamento.objects.all()
    return render(request, 'pdv/agendamentos.html', {'agendamentos': agendamentos})


# ➕ CRIAR AGENDAMENTO
@login_required
def criar_agendamento(request):
    form = AgendamentoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('agendamentos')

    return render(request, 'pdv/criar_agendamento.html', {'form': form})