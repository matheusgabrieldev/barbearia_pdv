from django.urls import path
from .views import *
from .views import agenda_semanal

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    path('', dashboard, name='dashboard'),

    path('clientes/', clientes_view, name='clientes'),
    path('clientes/criar/', criar_cliente, name='criar_cliente'),

    path('servicos/', servicos_view, name='servicos'),
    path('servicos/criar/', criar_servico, name='criar_servico'),

    path('agendamentos/', agendamentos_view, name='agendamentos'),
    path('agendamentos/criar/', criar_agendamento, name='criar_agendamento'),
    
    path('agenda/', agenda_semanal, name='agenda_semanal'),

]





