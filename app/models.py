from django.db import models
from cpf_field.models import CPFField
from django.utils.translation import gettext_lazy as _

AREA_CHOICES = (
    ('c', 'Contabilidade'),
    ('p', 'Plantio'),
    ('l', 'Colheita'),
    ('d', 'Distribuição'),
    ('i', 'Insumos')
)
AREA_MOTIVOS = (
    ('x', 'Nenhuma Opção'),
    ('F', 'Falecimento de cônjuge'),
    ('C', 'Licença de Casamento'),
    ('N', 'Nascimento de Filho'),
    ('D', 'Doação de Sangue Voluntária'),
    ('A', 'Alistamento Eleitoral'),
    ('S', 'Serviço Militar'),
    ('V', 'Vestibular'),
    ('M', 'Acompanhamento Médico'),
    ('E', 'Exames/Consultas Preventivas de Câncer'),
    ('O', 'Problemas de Saúde'),
    ('R', 'Reunião em organismo internacional')
)

class Funcionario(models.Model):
    nome = models.CharField(verbose_name=_('Nome'), max_length=255, null=False, blank=False)
    data_nascimento = models.DateField(verbose_name=_('Data de Nascimento'), null=False, blank=False)
    cpf = CPFField(verbose_name=_('CPF'), null=False, blank=False)
    endereco = models.CharField(verbose_name=_('Endereço'), max_length=100, null=False, blank=False)
    logradouro = models.CharField(verbose_name=_('Logradouro'), max_length=100, null=False, blank=False)
    complemento = models.CharField(verbose_name=_('Complemento'), max_length=100, blank=True) 
    funcao_exercida = models.CharField(verbose_name=_('Função Exercida'), max_length=100, null=False, blank=False)
    salario = models.DecimalField(verbose_name=_('Salário'), max_digits=8, decimal_places=2, null=False, blank=False, default=0.00)
    area_interesse = models.CharField(verbose_name=_('Área de Interesse'), max_length=1, choices=AREA_CHOICES, null=True, blank=True)
    password = models.CharField(verbose_name=_('Senha'), max_length=50, null=True)
    confirmpassword = models.CharField(verbose_name=_('Confirmar Senha'), max_length=50, null=True, blank=False)
    status_folga = models.CharField(verbose_name=_('Status de Folga'), max_length=100, default='0')

    def __str__(self):
        return self.nome
   
class GerenciaFolga(models.Model):
    cpf = CPFField(verbose_name=_('CPF'), null=False, blank=False) #Pegar o CPF e relacionar com o usuário cadastrado printando na interface "O usuário contêm X dias de folga"
    selectmotivo = models.CharField(verbose_name=_('Tipos de Licença'), max_length=1, choices=AREA_MOTIVOS, blank=False, null=True)
    motivo = models.TextField(verbose_name=_('Motivo'), max_length=500, null=False, blank=True)
    
    def __str__(self):
        return self.cpf
