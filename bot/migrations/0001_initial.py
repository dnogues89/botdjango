# Generated by Django 4.2.7 on 2023-12-05 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.IntegerField(unique=True)),
                ('nombre', models.CharField(blank=True, default='Estimado', max_length=50, null=True)),
                ('email', models.CharField(blank=True, default='sin@email.com', max_length=50, null=True)),
                ('flow', models.IntegerField(blank=True, null=True)),
                ('modelo', models.CharField(blank=True, default='Sin especificar', max_length=50, null=True)),
                ('canal', models.CharField(blank=True, max_length=50, null=True)),
                ('comentario', models.CharField(blank=True, default='Sin Comentario', max_length=1000, null=True)),
                ('contacto', models.DateTimeField(auto_now=True)),
                ('propuesta_crm', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('cant_contactos', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
            },
        ),
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error', models.TextField()),
                ('json', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flow_id', models.IntegerField()),
                ('respuesta_ok', models.TextField()),
                ('next_flow', models.IntegerField(blank=True, null=True)),
                ('respuesta_nook', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=100)),
                ('token', models.CharField(max_length=500)),
                ('id_wap', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MensajesRecibidos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_wa', models.CharField(max_length=100, unique=True)),
                ('mensaje', models.TextField()),
                ('timestamp', models.IntegerField()),
                ('telefono_receptor', models.CharField(max_length=100)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('json', models.JSONField(blank=True)),
                ('telefono_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.cliente')),
            ],
            options={
                'verbose_name': 'mensaje',
                'verbose_name_plural': 'mensajes',
            },
        ),
    ]