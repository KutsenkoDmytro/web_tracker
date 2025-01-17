# Generated by Django 4.2.1 on 2024-05-22 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Кампанія')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Кампанія',
                'verbose_name_plural': 'Кампанії',
            },
        ),
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Часова мітка')),
            ],
            options={
                'verbose_name': 'Клік',
                'verbose_name_plural': 'Кліки',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Офер')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('content', models.TextField(blank=True, verbose_name='Додатково')),
                ('cost_per_click', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна за клік')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Час створення')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Час зміни')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='ads.campaign', verbose_name='Кампанія')),
            ],
            options={
                'verbose_name': 'Офер',
                'verbose_name_plural': 'Офери',
            },
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Часова мітка')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP адреса')),
                ('operating_system', models.CharField(blank=True, max_length=100, null=True, verbose_name='Система')),
                ('user_agent', models.CharField(max_length=255, verbose_name='User-Agent')),
                ('geolocation', models.TextField(blank=True, null=True, verbose_name='Геолокація')),
                ('referrer', models.URLField(blank=True, null=True, verbose_name='Реферер')),
                ('email', models.EmailField(max_length=254, verbose_name='Електронна пошта')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефону')),
                ('click', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rel_lead', to='ads.click', verbose_name='Клік')),
            ],
            options={
                'verbose_name': 'Лід',
                'verbose_name_plural': 'Ліди',
            },
        ),
        migrations.AddField(
            model_name='click',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_click', to='ads.offer', verbose_name='Офер'),
        ),
    ]
