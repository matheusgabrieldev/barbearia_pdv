from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone



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

    clientes_count = Cliente.objects.count()
    servicos_count = Servico.objects.count()

    pagos = agendamentos.filter(status_pagamento="pago")
    total_vendas = sum(a.servico.preco for a in pagos)

    hoje = timezone.localdate()
    agendamentos_today = agendamentos.filter(data=hoje)

    next_agendamentos = agendamentos.order_by('data', 'horario')[:6]

    return render(request, 'pdv/dashboard.html', {
        'agendamentos': agendamentos,
        'clientes_count': clientes_count,
        'servicos_count': servicos_count,
        'total_vendas': total_vendas,
        'agendamentos_today': agendamentos_today,
        'next_agendamentos': next_agendamentos,
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


@login_required
def mudar_status_agendamento(request, id):

    agendamento = Agendamento.objects.get(id=id)

    if agendamento.status_pagamento == "pendente":
        agendamento.status_pagamento = "pago"

    elif agendamento.status_pagamento == "pago":
        pass  # já está pago, não faz nada

    elif agendamento.status_pagamento == "cancelado":
        return redirect('agendamentos')  # não permite mudar

    agendamento.save()

    return redirect('agendamentos')


# CRIAR AGENDA SEMANAL
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Agendamento


@login_required
def agenda_semanal(request):
    hoje = timezone.now()

    # Segunda-feira da semana atual
    dia_de_hoje = hoje.weekday()
    inicio_semana = hoje - timedelta(days=dia_de_hoje)
    inicio_semana = inicio_semana.replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # Domingo da semana
    fim_de_semana = inicio_semana + timedelta(days=6)
    fim_de_semana = fim_de_semana.replace(
        hour=23, minute=59, second=59, microsecond=999999
    )

    # Busca agendamentos da semana
    agendamentos = Agendamento.objects.filter(
        data__range=(inicio_semana, fim_de_semana)
    ).order_by('data', 'horario')

    # Organiza por dia
    agenda = {}

    for i in range(7):
        dia = inicio_semana + timedelta(days=i)

        # ✔️ CORREÇÃO AQUI (data é DateField)
        agenda[dia.date()] = agendamentos.filter(
            data=dia.date()
        )

    return render(request, 'pdv/agenda_semanal.html', {
        'agenda': agenda,
        'inicio_semana': inicio_semana,
        'fim_de_semana': fim_de_semana,
    })







































































