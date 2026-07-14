from django import forms
from django.core.validators import MinLengthValidator, RegexValidator
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
                'minlength': 5,  # ← HTML-валидация
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Минимум 20 символов',
            }),
        }
        # ✅ Подсказки под полями
        help_texts = {
            'title': 'Заголовок должен быть от 5 до 100 символов',
            'content': 'Содержание должно быть не менее 20 символов',
        }


# Форма с кастомной валидацией
class ContactForm(forms.Form):
    email = forms.EmailField(
        label='Ваш email',
        help_text='Принимаются только .ru, .com, .org домены',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.ru'
        })
    )
    
    passport = forms.CharField(
        label='Паспорт',
        min_length=10,
        max_length=11,
        help_text='Минимум 10 символов, формат: 1234 567890',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 567890'
        })
    )
    
    # ✅ Кастомная валидация конкретного поля
    def clean_passport(self):
        passport = self.cleaned_data.get('passport')
        if passport and not passport.replace(' ', '').isdigit():
            raise forms.ValidationError('Паспорт должен содержать только цифры')
        return passport
    
    # ✅ Кастомная валидация нескольких полей сразу
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        passport = cleaned_data.get('passport')
        
        if email and passport:
            # Пример сложной проверки
            if 'test' in email.lower() and len(passport) < 10:
                raise forms.ValidationError('Для тестовых email требуется полный паспорт')
        
        return cleaned_data