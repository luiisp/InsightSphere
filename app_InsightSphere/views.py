from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import User, Channel
from .forms.forms import ChannelForm
from django.views import View
import re


class Menu(View):
    allc = True

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            channels = Channel.objects.all()
        else:
            return redirect('home')

        return render(request, 'main/menu.html', {'user': user,
                                                   'channels': channels,
                                                   'view': self.allc})

    def post(self, request):
        if request.user.is_authenticated:
            x = request.POST.get('search')
            self.allc = False
            user = request.user
            channels = Channel.objects.filter(name__icontains=x)
            n = channels.count()
            result = (
                f'Não existe nenhum canal com este nome.' if n == 0
                else f'Foram foi encontrado {n} canal com esse nome.' if n == 1
                else f'Foram encontrados {n} canais com esse nome.'
            )
        else:
            return redirect('home')

        return render(request, 'main/menu.html', {'user': user,
                                                   'channels': channels,
                                                   'view': self.allc,
                                                   'result': result})


class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('menu')
        return render(request, 'home/home.html')


class Login(View):
    error_message = None

    def get(self, request):
        return render(request, 'account/login.html', {'error_message': self.error_message})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            self.error_message = 'Credenciais Incorretas'
        return render(request, 'account/login.html', {'error_message': self.error_message})


class NewAcc(View):
    pross = True
    pross2 = False
    error = None
    sit = 'Vamos criar sua conta!'

    def get(self, request):
        return render(request, 'account/newacc.html', {'pross': self.pross,
                                                       'pross2': self.pross2,
                                                       'error': self.error,
                                                       'sit': self.sit})

    def post(self, request):
        form_type = request.POST.get('form_type')
        if self.pross and form_type == 'pt1':
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            if not username or not email:
                self.error = 'Todos os campos devem ser preenchidos!'
            elif ' ' in username:
                self.error = 'O nome de usuário não pode conter espaços'
            elif len(username) <= 3:
                self.error = 'O nome de usuário deve ter pelo menos 4 caracteres!'
            elif username.count('_') > 2 or username.count('.') > 2:
                self.error = 'O nome de usuário não pode ter mais de dois _ ou .'
            elif not re.match(r'^[a-zA-Z0-9_.]+$', username):
                self.error = 'O nome de usuário deve conter apenas letras, números, _, ou .'
            elif User.objects.filter(username=username).exists():
                self.error = 'Já existe um usuário com esse nome de usuário :/'
            elif User.objects.filter(email=email).exists():
                self.error = 'Este e-mail já está associado a uma conta!'
            else:
                self.sit = ''
                self.pross2 = True
                self.pross = False
                request.session['username'] = username
                request.session['email'] = email
                request.session['pass?'] = True

        if form_type == 'pt2':
            username = request.session['username']
            email = request.session['email']
            self.pross = False
            self.pross2 = True
            apelido = request.POST.get('apelido', '')
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            if password != password2:
                self.error = 'As senhas não coincidem!'
            else:
                self.sit = 'Sua conta está sendo criada!'
                self.ok = True
                self.pross = False
                self.pross2 = False

            if request.session['pass?']:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.apelido = apelido
                user.save()
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('menu')

        return render(request, 'account/newacc.html', {'pross': self.pross,
                                                       'pross2': self.pross2,
                                                       'error': self.error,
                                                       'sit': self.sit})


def auth_anonim(request):
    User = get_user_model()

    user, created = User.objects.get_or_create(username='Anonymous')

    apelido = request.POST.get('apelido')
    if apelido:
        user.apelido = apelido
        user.save()
    else:
        user.apelido = 'Anonymous'
        user.save()
    return user


class Anonim(View):
    def get(self, request):
        return render(request, 'account/anonim.html')

    def post(self, request):
        user = auth_anonim(request)
        login(request, user)
        return redirect('menu')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class NewChannel(View):
    template = 'channel/newchannel.html'

    def get(self, request):
        form = ChannelForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        ir = False
        error = 'a'
        form_data = {
            'name': request.POST.get('name', ''),
            'description': request.POST.get('description', '')
        }
        if not 3 <= len(form_data['name']) <= 18:
            error = 'O nome do canal deve ter entre 3 e 18 caracteres!'
        elif not 3 <= len(form_data['description']) <= 28:
            error = 'A descrição do canal deve ter entre 3 e 28 caracteres!'
        else:
            count = Channel.objects.filter(creator=request.user).count()

            if count >= 2:
                error = 'Cada usuário só pode ter dois canais!'
            else:
                ir = True

        form = ChannelForm(data=form_data)
        if ir and form.is_valid():
            channel = form.save(commit=False)
            channel.creator = request.user
            channel.save()
            id_channel = channel.id
            return redirect('channel_detail', username=request.user.username, channel_id=id_channel)

        return render(request, self.template, {'form': form,
                                               'error': error})


class Channel_V(View):
    def get(self, request, username, channel_id):
        if not request.user.is_authenticated:
            return redirect('home')

        channel = get_object_or_404(Channel, id=channel_id)
        channel_info = {
            'name': channel.name,
            'description': channel.description,
            'creator': channel.creator,
            'id': channel_id,
            'verified': channel.verified
        }

        return render(request, 'channel/channel.html', {'dono': username,
                                                        'canal': channel_info,
                                                        'user': request.user,
                                                        'verificado': {channel.verified}})


class Delete(View):
    def get(self, request, channel_id):
        channel = get_object_or_404(Channel, id=channel_id)
        if channel.creator == request.user:
            channel.delete()
        return redirect('menu')


class User_V(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        channels = Channel.objects.filter(creator=user)
        owner_info = {
            'username': f'@{user.username}',
            'apelido': user.apelido,
            'join': user.date_joined.strftime('%H:%M %d/%m/%Y') if user.date_joined is not None else 'Indefinido',
            'last_login': user.last_login.strftime('%H:%M %d/%m/%Y') if user.last_login is not None else 'Indefinido',
            'staff': user.is_staff,
            'channels': channels
        }

        return render(request, 'user/user.html', {'owner': owner_info})
