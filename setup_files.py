import os

# Базовая директория проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Словарь с путями и содержимым файлов
files_to_create = {
    # 1. Модели
    "blog/models.py": """from django.db import models

class Post(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    content = models.TextField('Содержание')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
""",

    # 2. Формы
    "blog/forms.py": """from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите содержание поста'}),
        }
""",

    # 3. Представления (Views)
    "blog/views.py": """from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

def home(request):
    return render(request, 'blog/home.html')

def about(request):
    return render(request, 'blog/about.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
""",

    # 4. Маршруты приложения
    "blog/urls.py": """from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
""",

    # 5. Главные маршруты проекта
    "myblog/urls.py": """from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
""",

    # 6. Тесты (Обязательное требование ТЗ!)
    "blog/tests.py": """from django.test import TestCase
from django.urls import reverse
from .models import Post

class BlogViewsTestCase(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Тест', content='Текст')

    def test_home_view(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тест')

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Текст')
""",

    # 7. Шаблоны
    "blog/templates/blog/base.html": """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Мой Блог{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/blog/css/style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
        <div class="container">
            <a class="navbar-brand fw-bold" href="{% url 'blog:home' %}">📖 Мой Блог</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{% url 'blog:home' %}">Главная</a>
                <a class="nav-link" href="{% url 'blog:about' %}">О нас</a>
                <a class="nav-link" href="{% url 'blog:post_list' %}">Посты</a>
                <a class="nav-link btn btn-light text-primary ms-2 px-3" href="{% url 'blog:post_create' %}">+ Новый пост</a>
            </div>
        </div>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
    <footer class="bg-dark text-white text-center py-3 mt-5">
        <p class="mb-0">© 2026 Виктор Куличенко. Тема #16: View и URLS</p>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""",

    "blog/templates/blog/home.html": """{% extends 'blog/base.html' %}
{% block title %}Главная{% endblock %}
{% block content %}
<div class="text-center py-5">
    <h1 class="display-4">Добро пожаловать в мой блог!</h1>
    <p class="lead">Демонстрация работы с маршрутами и представлениями Django.</p>
    <a href="{% url 'blog:about' %}" class="btn btn-primary btn-lg me-2">О нас</a>
    <a href="{% url 'blog:post_list' %}" class="btn btn-outline-primary btn-lg">Список постов</a>
</div>
{% endblock %}
""",

    "blog/templates/blog/about.html": """{% extends 'blog/base.html' %}
{% block title %}О нас{% endblock %}
{% block content %}
<div class="card p-4">
    <h2>О проекте</h2>
    <p>Этот блог создан в рамках задания по теме "View и URLS. Представление и маршруты".</p>
    <h4>Что реализовано:</h4>
    <ul>
        <li>Простые и динамические маршруты</li>
        <li>Class-Based Views (ListView, DetailView, CreateView, UpdateView, DeleteView)</li>
        <li>Формы с валидацией данных</li>
        <li>CSS-стилизация через Bootstrap 5</li>
        <li>Тесты для проверки маршрутов</li>
    </ul>
</div>
{% endblock %}
""",

    "blog/templates/blog/post_list.html": """{% extends 'blog/base.html' %}
{% block title %}Список постов{% endblock %}
{% block content %}
<h2 class="mb-4">Все посты</h2>
{% if posts %}
    <div class="row">
        {% for post in posts %}
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">
                        <a href="{% url 'blog:post_detail' post.pk %}" class="text-decoration-none">{{ post.title }}</a>
                    </h5>
                    <p class="text-muted small">📅 {{ post.created_at|date:"d.m.Y H:i" }}</p>
                    <p class="card-text">{{ post.content|truncatewords:20 }}</p>
                    <a href="{% url 'blog:post_detail' post.pk %}" class="btn btn-sm btn-primary">Читать далее</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
{% else %}
    <div class="alert alert-info">Постов пока нет. <a href="{% url 'blog:post_create' %}">Создайте первый!</a></div>
{% endif %}
{% endblock %}
""",

    "blog/templates/blog/post_detail.html": """{% extends 'blog/base.html' %}
{% block title %}{{ post.title }}{% endblock %}
{% block content %}
<div class="card p-4">
    <h2>{{ post.title }}</h2>
    <p class="text-muted">📅 {{ post.created_at|date:"d.m.Y в H:i" }}</p>
    <hr>
    <p class="fs-5">{{ post.content|linebreaks }}</p>
    <hr>
    <div class="d-flex gap-2">
        <a href="{% url 'blog:post_list' %}" class="btn btn-secondary">← Назад</a>
        <a href="{% url 'blog:post_update' post.pk %}" class="btn btn-warning">✏️ Редактировать</a>
        <a href="{% url 'blog:post_delete' post.pk %}" class="btn btn-danger">🗑️ Удалить</a>
    </div>
</div>
{% endblock %}
""",

    "blog/templates/blog/post_form.html": """{% extends 'blog/base.html' %}
{% block title %}{% if object %}Редактирование{% else %}Создание{% endif %} поста{% endblock %}
{% block content %}
<div class="card p-4" style="max-width: 600px; margin: 0 auto;">
    <h2 class="mb-4">{% if object %}Редактировать пост{% else %}Создать новый пост{% endif %}</h2>
    <form method="post">
        {% csrf_token %}
        {% if form.errors %}
            <div class="alert alert-danger">
                <strong>Ошибка!</strong> Пожалуйста, исправьте данные ниже.
                {{ form.errors }}
            </div>
        {% endif %}
        <div class="mb-3">
            <label class="form-label">Заголовок</label>
            {{ form.title }}
        </div>
        <div class="mb-3">
            <label class="form-label">Содержание</label>
            {{ form.content }}
        </div>
        <button type="submit" class="btn btn-primary w-100">Сохранить</button>
    </form>
</div>
{% endblock %}
""",

    "blog/templates/blog/post_confirm_delete.html": """{% extends 'blog/base.html' %}
{% block title %}Удаление поста{% endblock %}
{% block content %}
<div class="card p-4 text-center" style="max-width: 500px; margin: 0 auto;">
    <h2 class="text-danger">Подтверждение удаления</h2>
    <p>Вы уверены, что хотите удалить пост "<strong>{{ post.title }}</strong>"?</p>
    <form method="post">
        {% csrf_token %}
        <div class="d-flex justify-content-center gap-3">
            <a href="{% url 'blog:post_detail' post.pk %}" class="btn btn-secondary">Отмена</a>
            <button type="submit" class="btn btn-danger">Да, удалить</button>
        </div>
    </form>
</div>
{% endblock %}
""",

    # 8. CSS стили (Обязательное требование ТЗ!)
    "blog/static/blog/css/style.css": """body { background-color: #f8f9fa; }
.card { box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: none; transition: transform 0.2s; }
.card:hover { transform: translateY(-3px); }
.navbar-brand { font-size: 1.4rem; }
.display-4 { color: #0d6efd; }
"""
}

# Создание директорий и запись файлов
for file_path, content in files_to_create.items():
    full_path = os.path.join(BASE_DIR, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Создан/обновлен: {file_path}")

print("\n🎉 Все файлы успешно созданы! Теперь можно делать миграции.")