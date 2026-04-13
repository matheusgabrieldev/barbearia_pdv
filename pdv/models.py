from django.db import models


# 👤 CLIENTE
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)

    def __str__(self):
        return self.nome


# 💈 SERVIÇO
class Servico(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome


# 📅 AGENDAMENTO
class Agendamento(models.Model):
    
    STATUS_AGENDADO = 'agendado'
    STATUS_EM_ANDAMENTO = 'em_andamento'
    STATUS_FINALIZADO = 'finalizado'
    STATUS_CANCELADO = 'cancelado'

    STATUS_CHOICES = [
        (STATUS_AGENDADO, 'Agendado'),
        (STATUS_EM_ANDAMENTO, 'Em andamento'),
        (STATUS_FINALIZADO, 'Finalizado'),
        (STATUS_CANCELADO, 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()
    
    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default=STATUS_AGENDADO,
)

    def __str__(self):
        return f"{self.cliente} - {self.servico} - {self.data} - {self.horario}"
