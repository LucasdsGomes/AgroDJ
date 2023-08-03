from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import FuncionarioForm , GerenciaFolgaForm
from datetime import date
from django.contrib import messages
from .models import Funcionario, AREA_CHOICES, GerenciaFolga
from django.utils.translation import gettext_lazy as _
from datetime import date

def folga(request):
    if request.method == 'POST':
        form = GerenciaFolgaForm(request.POST)
        cpf = request.POST.get('cpf')
        selectmotivo = request.POST.get('selectmotivo')
        
        if selectmotivo == "x":
            status_folga = ""
        elif selectmotivo == "F":
            status_folga = "2"
        elif selectmotivo == "C":
            status_folga = "3"
        elif selectmotivo == "N":
            status_folga = "5"
        elif selectmotivo == "D":
            status_folga = "1"
        elif selectmotivo == "A":
            status_folga = "2"
        elif selectmotivo in ["S", "V"]:
            status_folga = "Tempo do cumprimento das exigências solicitadas"
        elif selectmotivo == "M":
            status_folga = "2"
        elif selectmotivo == "E":
            status_folga = "3"
        elif selectmotivo in ["O", "R"]:
            status_folga = "Dias determinados no atestado médico" if selectmotivo == "O" else "Durante o tempo necessário da participação"
        
        if not Funcionario.objects.filter(cpf=cpf).exists():
            messages.error(request, "O CPF não existe!")
        elif form.is_valid():
            funcionario = Funcionario.objects.get(cpf=cpf)
            
            # Atualizar o motivo de folga apenas se o motivo for selecionado
            if selectmotivo != "x":
                funcionario.status_folga = status_folga
                funcionario.save()
                
                # Remover motivos anteriores para o mesmo CPF
                GerenciaFolga.objects.filter(cpf=cpf).delete()
                
                # Adicionar o novo motivo
                form.instance.cpf = cpf
                form.instance.motivo = status_folga
                form.save()
                
                messages.success(request, "Sua licença foi atualizada em nosso sistema! Verifique o status na página home.")
            else:
                messages.error(request, "Selecione um motivo válido ou escreva um motivo para aprovarmos sua licença.")
                return redirect('folga')
                
            return redirect('home')
    else:
        form = GerenciaFolgaForm()
    
    folga_queryset = GerenciaFolga.objects.all()
    
    return render(request, 'folga.html', {'folga_queryset': folga_queryset, 'form': form})


    

def home(request):
    folga_queryset = GerenciaFolga.objects.all()  # Adicione essa linha
    funcionarios = Funcionario.objects.all()
    return render(request, 'home.html', {'funcionarios': funcionarios, 'folga_queryset': folga_queryset})

def register(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)

        nome = request.POST.get('nome')
        confirmpassword = request.POST.get('confirmpassword')
        password = request.POST.get('password')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        
        if Funcionario.objects.filter(cpf=cpf).exists():
            messages.error(request, "O CPF já existe!")
        elif form.is_valid() and confirmpassword == password:
            try:
                birth_date = date.fromisoformat(data_nascimento)
                today = date.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                if age < 18:
                    messages.error(request, "O usuário têm de ser maior de 18.")
                elif age > 110:
                    messages.error(request, "O usuário não pode ter mais de 110 anos.")
                else:
                    form.save()
                    user = User.objects.create_user(username=cpf, password=confirmpassword)
                    user.first_name = nome
                    user.save()

                    user = authenticate(request, username=cpf, password=confirmpassword)
                    if user is not None:
                        login(request, user)

                    return redirect('home')
            except ValueError:
                messages.error(request, "Data de nascimento inválida. Use o formato AAAA-MM-DD.")
        else:
            messages.error(request, "As senhas não coincidem. Há erros no formulário.")
    else:
        form = FuncionarioForm()

    return render(request, 'register.html', {'form': form, 'AREA_CHOICES': AREA_CHOICES})

def edit(request, id):
    funcionario = Funcionario.objects.get(id=id)
    return render(request, 'edit.html', {'funcionario': funcionario, 'AREA_CHOICES': AREA_CHOICES})


def update(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        
        if form.is_valid():
            nome = form.cleaned_data['nome']
            cpf = form.cleaned_data['cpf']
            salario = form.cleaned_data['salario']
            data_nascimento = form.cleaned_data['data_nascimento']
            endereco = form.cleaned_data['endereco']
            complemento = form.cleaned_data['complemento']
            area_interesse = form.cleaned_data['area_interesse']
            funcao_exercida = form.cleaned_data['funcao_exercida']
            logradouro = form.cleaned_data['logradouro']
            password = form.cleaned_data['password']
            confirmpassword = form.cleaned_data['confirmpassword']
            
            if not cpf.isdigit():
                messages.error(request, "O campo CPF deve conter apenas números.")
                return render(request, 'edit.html', {'funcionario': funcionario, 'form': form, 'AREA_CHOICES':AREA_CHOICES})
            
            if not Funcionario.objects.filter(cpf=cpf).exists():
                messages.error(request, "Você não pode alterar o CPF já cadastrado.")
                return render(request, 'edit.html', {'funcionario': funcionario, 'form': form, 'AREA_CHOICES':AREA_CHOICES})

            if not nome.replace(" ", "").isalpha():
                messages.error(request, "O campo Nome deve conter apenas letras e espaços.")
                return render(request, 'edit.html', {'funcionario': funcionario, 'form': form, 'AREA_CHOICES': AREA_CHOICES})

            try:
                salario = float(salario)
            except ValueError:
                messages.error(request, "O campo Salário deve conter apenas números.")
                return render(request, 'edit.html', {'funcionario': funcionario, 'form': form, 'AREA_CHOICES':AREA_CHOICES})

            birth_date = data_nascimento
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            
            if age < 18:
                messages.error(request, "Você tem de ser mais de 18 anos para entrar.")
            elif age > 110:
                messages.error(request, "O usuário não pode ter mais de 110 anos.")
            else:
                funcionario.nome = nome
                funcionario.cpf = cpf
                funcionario.data_nascimento = data_nascimento
                funcionario.endereco = endereco
                funcionario.logradouro = logradouro
                funcionario.complemento = complemento
                funcionario.funcao_exercida = funcao_exercida
                funcionario.salario = salario
                funcionario.area_interesse = area_interesse
                funcionario.password = password
                funcionario.confirmpassword = confirmpassword
                funcionario.save()
                messages.success(request, "A alteração foi feita com sucesso!")
                return redirect('home')
        else:
            messages.error(request, "O formulário não está válido")
    else:
        form = FuncionarioForm(instance=funcionario)

    return render(request, 'edit.html', {'funcionario': funcionario, 'form': form, 'AREA_CHOICES':AREA_CHOICES})



def delete(request, id):
    funcionario = Funcionario.objects.get(id=id)
    funcionario.delete()
    return redirect('home')

def logging(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        password = request.POST.get('password')

        # Authenticate the user using the cpf as username
        user = authenticate(request, username=cpf, password=password)

        if user is not None:
            # Login the user if authentication is successful
            login(request, user)
            messages.success(request, "Você efetuou o login com sucesso!")
            return redirect('home')
        else:
            messages.error(request, "Credenciais inválidas. Por favor, verifique seu usuário e senha.")
            return redirect('home')
    else:
        messages.error(request, "Ocorreu um erro, tente novamente")
        return redirect('home')


def logout(request):
    if request.method == 'POST' and 'logout-btn' in request.POST:
        auth_logout(request)
        return redirect('home')
    else:
        messages.error(request, "Ação inválida de logout. Por favor, utilize o botão de logout.")
        return redirect('home')
    
    
def section(request):
    return render(request, 'section.html') 

def cont(request):
    if request.method == 'POST':
        area = request.POST.get("c")
        if area == "Contabilidade": 
            nome = request.POST.get("nome")
            data_nascimento = request.POST.get("data_nascimento")
            cpf = request.POST.get("cpf")
            salario = request.POST.get("salario")
            funcionarios = Funcionario.objects.filter(nome=nome, data_nascimento=data_nascimento, cpf=cpf, area=area, salario=salario)            
            for funcionario in funcionarios:
                funcionario.save()
    else:
        funcionarios = Funcionario.objects.all()
        
    return render(request, 'cont.html', {'funcionarios': funcionarios}) 

def plant(request):
    if request.method == 'POST':
        area = request.POST.get("p")
        if area == "Plantio": 
            nome = request.POST.get("nome")
            data_nascimento = request.POST.get("data_nascimento")
            cpf = request.POST.get("cpf")
            salario = request.POST.get("salario")
            funcionarios = Funcionario.objects.filter(nome=nome, data_nascimento=data_nascimento, cpf=cpf, area=area, salario=salario)            
            for funcionario in funcionarios:
                funcionario.save()
    else:
        funcionarios = Funcionario.objects.all()
        
    return render(request, 'plant.html', {'funcionarios': funcionarios}) 

def colhen(request):
    if request.method == 'POST':
        area = request.POST.get("l")
        if area == "Colheita": 
            nome = request.POST.get("nome")
            data_nascimento = request.POST.get("data_nascimento")
            cpf = request.POST.get("cpf")
            salario = request.POST.get("salario")
            funcionarios = Funcionario.objects.filter(nome=nome, data_nascimento=data_nascimento, cpf=cpf, area=area, salario=salario)            
            for funcionario in funcionarios:
                funcionario.save()
    else:
        funcionarios = Funcionario.objects.all()
        
    return render(request, 'colhen.html', {'funcionarios': funcionarios}) 
    
def insum(request):
    if request.method == 'POST':
        area = request.POST.get("i")
        if area == "Insumos": 
            nome = request.POST.get("nome")
            data_nascimento = request.POST.get("data_nascimento")
            cpf = request.POST.get("cpf")
            salario = request.POST.get("salario")
            funcionarios = Funcionario.objects.filter(nome=nome, data_nascimento=data_nascimento, cpf=cpf, area=area, salario=salario)            
            for funcionario in funcionarios:
                funcionario.save()
    else:
        funcionarios = Funcionario.objects.all()
        
    return render(request, 'insum.html', {'funcionarios': funcionarios}) 
    
def dist(request):
    if request.method == 'POST':
        area = request.POST.get("d")
        if area == "Distribuição": 
            nome = request.POST.get("nome")
            data_nascimento = request.POST.get("data_nascimento")
            cpf = request.POST.get("cpf")
            salario = request.POST.get("salario")
            funcionarios = Funcionario.objects.filter(nome=nome, data_nascimento=data_nascimento, cpf=cpf, area=area, salario=salario)            
            for funcionario in funcionarios:
                funcionario.save()
    else:
        funcionarios = Funcionario.objects.all()
        
    return render(request, 'dist.html', {'funcionarios': funcionarios}) 





    