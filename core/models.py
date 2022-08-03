from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

MALE = 'M'
FEMALE = 'F'

GENDERS = (
    (MALE, 'Мужской'),
    (FEMALE, 'Женский')
)


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата добавление') 
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата изменения')

    class Meta:
        abstract = True


class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, phone_number, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен быть назначен is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен быть назначен is_superuser=True.')

        return self.create_user(phone_number, password, **other_fields)

    def create_user(self, phone_number, password, **other_fields):

        user = self.model(phone_number=phone_number, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Teacher(AbstractBaseUser, PermissionsMixin, TimeStampMixin):

    class Meta:
        verbose_name = "учитель"
        verbose_name_plural = 'учителя'
        ordering = ('-created_at', '-updated_at')

    avatar = models.ImageField(upload_to='avatars/', verbose_name='аватарка', null=True, blank=True)
    phone_number = models.CharField(max_length=10, verbose_name='номер телефона', unique=True)
    name = models.CharField(max_length=150, blank=True, verbose_name='полная имя')
    gender = models.CharField(max_length=1, verbose_name='пол', choices=GENDERS, default=MALE)
    email = models.EmailField(verbose_name='элетронная почта', null=True, blank=True)
    group = models.OneToOneField('Group', verbose_name='класс', 
                    on_delete=models.SET_NULL, null=True, related_name='set_teacher')
    
    is_staff = models.BooleanField(default=True, verbose_name='статус персонала')
    is_active = models.BooleanField(default=True, verbose_name='подтверждение по почте')
    is_superuser = models.BooleanField(default=False, verbose_name='cтатус администратора')
    objects = CustomAccountManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.phone_number}'


class Student(TimeStampMixin):

    class Meta:
        verbose_name = 'ученик'
        verbose_name_plural = 'ученики'
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(max_length=50, verbose_name='ФИО')
    email = models.EmailField(verbose_name='элетронная почта')
    birthday = models.DateField(verbose_name='дата рождения')
    group = models.ForeignKey('Group', verbose_name='класс', on_delete=models.SET_NULL, null=True,)
    address = models.CharField(max_length=50, verbose_name='адрес')
    gender = models.CharField(max_length=1, verbose_name='пол', choices=GENDERS, default=MALE)
    photo = models.ImageField(verbose_name='фото ученика', upload_to='students/', 
                                                                blank=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name='подтверждение')                                                    

    def __str__(self):
        return f'{self.name}'


class Group(TimeStampMixin):

    class Meta:
        verbose_name = 'класс'
        verbose_name_plural = 'классы'
        ordering = ('-created_at', '-updated_at')
    
    title = models.CharField(max_length=15, verbose_name='название класса')
    teacher = models.OneToOneField('Teacher', verbose_name='классный руководитель', blank=True, 
                on_delete=models.SET_NULL, null=True, related_name='set_group', default=None)
    students = models.ManyToManyField('Student', verbose_name='ученики',
                                         blank=True, related_name='set_group')

    def __str__(self):
        return f'{self.title}'


class School(TimeStampMixin):
    
    class Meta:
        verbose_name = 'школа'
        verbose_name_plural = 'школы'
        ordering = ('-created_at', '-updated_at')

    title = models.CharField(max_length=50, verbose_name='название школы')
    groups = models.ManyToManyField('Group', verbose_name='классы', related_name='set_school', blank=True)

    def __str__(self):
        return f'{self.title}'
    

# Create your models here.
