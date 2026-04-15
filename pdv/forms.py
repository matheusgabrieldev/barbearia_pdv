from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Servico, Agendamento


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone']


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'preco']


class AgendamentoForm(forms.ModelForm):
    
    def clean(self):
        
        cleaned_data = super().clean()
        data = cleaned_data.get('data')   
        horario = cleaned_data.get('horario')
        if data and horario:
            if Agendamento.objects.filter(data=data, horario=horario).exists():
                raise forms.ValidationError("Já existe um agendamento para este dia e horário.")
        return cleaned_data
    
    class Meta:
        model = Agendamento
        fields = ['cliente', 'servico', 'data', 'horario', 'status_atendimento', 'status_pagamento' ]
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }


class CriarAgendamentoForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        horario = cleaned_data.get('horario')

        if data and horario:
            conflito = Agendamento.objects.filter(
                data=data,
                horario=horario,
                status_atendimento__in=[
                    Agendamento.STATUS_AGENDADO,
                    Agendamento.STATUS_EM_ANDAMENTO
                ]
            ).exists()

            if conflito:
                raise forms.ValidationError("Já existe um agendamento ativo nesse horário.")

        return cleaned_data
    
    class Meta:
        model = Agendamento
        fields = ['cliente', 'servico', 'data', 'horario']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Senhas não coincidem")