# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 02:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Asistente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(blank=True, max_length=40)),
                ('Escuela', models.CharField(blank=True, max_length=40)),
                ('Correo', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Categoria', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Comentario', models.TextField()),
                ('Fecha', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Titulo', models.CharField(max_length=50)),
                ('DescripcionL', models.TextField()),
                ('DescripcionC', models.CharField(max_length=150)),
                ('Fecha', models.DateField()),
                ('Hora', models.TimeField()),
                ('Publicado', models.BooleanField(default=False)),
                ('Vistas', models.IntegerField(default=0)),
                ('Lugar', models.CharField(default='Teatro Calafornix', max_length=40)),
                ('PlaceID', models.CharField(blank=True, max_length=27)),
            ],
        ),
        migrations.CreateModel(
            name='EventosEsperados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Evento', models.ManyToManyField(blank=True, to='home.Evento')),
            ],
        ),
        migrations.CreateModel(
            name='EventosGuardados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Evento', models.ManyToManyField(blank=True, to='home.Evento')),
            ],
        ),
        migrations.CreateModel(
            name='Imagenes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Imagen', models.ImageField(upload_to='eventos')),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Usuario', models.CharField(max_length=40)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tipo', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=40)),
                ('ApellidoPaterno', models.CharField(max_length=40)),
                ('ApellidoMaterno', models.CharField(max_length=40)),
                ('Correo', models.EmailField(max_length=254)),
                ('Direccion', models.CharField(blank=True, max_length=40)),
                ('Telefono', models.CharField(blank=True, max_length=40)),
                ('PaginaWeb', models.CharField(blank=True, max_length=50)),
                ('NumControl', models.CharField(blank=True, max_length=8)),
                ('Tipo', models.CharField(choices=[('A', 'Alumno'), ('B', 'Admin'), ('C', 'Externo'), ('D', 'Interno')], max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='Usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Usuario'),
        ),
        migrations.AddField(
            model_name='eventosguardados',
            name='Usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.Usuario'),
        ),
        migrations.AddField(
            model_name='eventosesperados',
            name='Usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.Usuario'),
        ),
        migrations.AddField(
            model_name='evento',
            name='Autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Usuario'),
        ),
        migrations.AddField(
            model_name='evento',
            name='Categorias',
            field=models.ManyToManyField(to='home.Categoria'),
        ),
        migrations.AddField(
            model_name='evento',
            name='Comentarios',
            field=models.ManyToManyField(blank=True, to='home.Comentario'),
        ),
        migrations.AddField(
            model_name='evento',
            name='Imagenes',
            field=models.ManyToManyField(blank=True, to='home.Imagenes'),
        ),
        migrations.AddField(
            model_name='evento',
            name='Likes',
            field=models.ManyToManyField(blank=True, to='home.Like'),
        ),
        migrations.AddField(
            model_name='evento',
            name='Tipos',
            field=models.ManyToManyField(blank=True, to='home.Tipo'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='Usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Usuario'),
        ),
        migrations.AddField(
            model_name='asistente',
            name='Usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Usuario'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='Asistentes',
            field=models.ManyToManyField(blank=True, to='home.Asistente'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='Evento',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.Evento'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='Staff',
            field=models.ManyToManyField(blank=True, to='home.Staff'),
        ),
    ]
