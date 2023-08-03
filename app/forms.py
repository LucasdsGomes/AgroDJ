from django import forms
from .models import Funcionario, GerenciaFolga, AREA_MOTIVOS

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__'
        exclude = ['status_folga']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Data de Nascimento (YYYY-MM-DD)'}),
            'nome': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Nome Completo'}),
            'cpf': forms.TextInput(attrs={'type': 'text', 'placeholder': 'CPF'}),
            'endereco': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Endereço'}),
            'logradouro': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Logradouro'}),
            'complemento': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Complemento'}),
            'funcao_exercida': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Função Exercida'}),
            'salario': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Salário'}),
            'password': forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'Senha'}),
            'confirmpassword': forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'Confirme sua senha'}),
        }

class GerenciaFolgaForm(forms.ModelForm):
    selectmotivo = forms.ChoiceField(choices=AREA_MOTIVOS, label='Tipos de Licença')

    class Meta:
        model = GerenciaFolga
        fields = '__all__'
        widgets = {
            'cpf': forms.TextInput(attrs={'type': 'text', 'placeholder': 'CPF'}),
            'selectmotivo': forms.Select,
            'motivo': forms.Textarea(attrs={'placeholder': 'Motivo'}),
        }
