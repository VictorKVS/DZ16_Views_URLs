from django.db import models
from django.core.validators import (
    MinLengthValidator, 
    MaxLengthValidator, 
    RegexValidator,
    EmailValidator
)


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    content = models.TextField('Содержание')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# Пример модели пользователя с валидацией
class UserProfile(models.Model):
    # ✅ Email — встроенная проверка формата
    email = models.EmailField(
        'Email',
        validators=[EmailValidator(message='Введите корректный email (например: user@mail.ru)')]
    )
    
    # ✅ Паспорт — минимум 10 символов, только цифры
    passport = models.CharField(
        'Серия и номер паспорта',
        max_length=11,
        validators=[
            MinLengthValidator(10, message='Паспорт должен содержать минимум 10 символов'),
            RegexValidator(
                regex=r'^\d{4}\s?\d{6}$',
                message='Формат: 1234 567890 (4 цифры, пробел, 6 цифр)'
            )
        ],
        help_text='Введите серию и номер в формате: 1234 567890'  # ← подсказка под полем
    )
    
    # ✅ Телефон — только цифры
    phone = models.CharField(
        'Телефон',
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^\+7\d{10}$',
                message='Формат: +79991234567'
            )
        ],
        help_text='Формат: +7XXXXXXXXXX'
    )

    def __str__(self):
        return self.email