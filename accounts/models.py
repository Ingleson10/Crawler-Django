from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from plans.models import Plan

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo Email deve ser definido')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=100, blank=False, verbose_name='E-mail')
    first_name = models.CharField(max_length=50, blank=False, verbose_name='Nome')
    last_name = models.CharField(max_length=100, blank=False, verbose_name='Sobrenome')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    is_active = models.BooleanField(default=True, verbose_name='Usuário Ativo')
    is_staff = models.BooleanField(default=False, verbose_name='Admin')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.email


class Subscription(models.Model):

    STATUS_CHOICES = (
        ('active', 'Ativa'),
        ('cancelled', 'Cancelada'),
        ('expired', 'Expirada'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name='Plano')
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de Início')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Data Final')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = (
        ('completed', 'Concluído'),
        ('failed', 'Negado'),
        ('pending', 'Pendente'),
    )
    
    STATUS_CHOICES = (
        ('credit_card', 'Cartão de Crédito'),
        ('paypal', 'PayPal'),
    )
    
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name='Inscrição')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name='Forma de Pagamento')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Data do Pagamento')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    message = models.TextField(null=False, verbose_name='Mensagem')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criada em')
    read = models.BooleanField(default=False, verbose_name='Ler')

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'


class SupportTicket(models.Model):

    STATUS_CHOICES = (
        ('open', 'Aberto'),
        ('in_progress', 'Em andamento'),
        ('closed', 'Fechado'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    subject = models.CharField(max_length=100, null=False, verbose_name='Assunto')
    description = models.TextField(null=False, verbose_name='Descrição')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criada em')

    class Meta:
        verbose_name = 'Ticket de Suporte'
        verbose_name_plural = 'Tickets de Suporte'
