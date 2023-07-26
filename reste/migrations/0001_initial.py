# Generated by Django 4.2.2 on 2023-07-25 09:19

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
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnfl', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('passport_number', models.IntegerField()),
                ('issued', models.CharField(max_length=100)),
                ('date_issue', models.DateTimeField()),
                ('goden', models.IntegerField()),
                ('nation', models.CharField(max_length=100)),
                ('citizienship', models.CharField(max_length=100)),
                ('whos_addres', models.CharField(max_length=100)),
                ('addres', models.TextField()),
                ('whos_number', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('card_number', models.IntegerField()),
                ('card_term', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_merchant', models.CharField(max_length=100)),
                ('name_shop', models.CharField(max_length=100)),
                ('phone_number', models.IntegerField()),
                ('addres', models.TextField()),
                ('name_bank', models.CharField(max_length=100)),
                ('mfo', models.IntegerField()),
                ('bank_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('rassrochka', models.DateTimeField(auto_now_add=True)),
                ('every_pays', models.TextField()),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('own_partifition', models.IntegerField()),
                ('installment_balance', models.IntegerField()),
                ('status', models.CharField(max_length=100)),
                ('owner', models.CharField(max_length=100)),
                ('number_cart', models.IntegerField()),
                ('valid_about', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('firm', models.CharField(max_length=100)),
                ('model_product', models.CharField(max_length=100)),
                ('ikpu_product', models.CharField(max_length=100)),
                ('color_product', models.CharField(max_length=100)),
                ('country_manufacture', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('password', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Telev',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_model', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('dogovor', models.BooleanField()),
                ('email', models.EmailField(max_length=254)),
                ('characteristics', models.TextField()),
                ('telev', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reste.product')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reste.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Shopping Card',
                'verbose_name_plural': 'Shopping Cards',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_model', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('dogovor', models.BooleanField()),
                ('email', models.EmailField(max_length=254)),
                ('characteristics', models.TextField()),
                ('memory', models.IntegerField()),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reste.product')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_model', models.TextField()),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('dogovor', models.BooleanField()),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=100)),
                ('characteristics', models.TextField()),
                ('phone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reste.product')),
            ],
        ),
        migrations.CreateModel(
            name='Komp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_model', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('dogovor', models.BooleanField()),
                ('email', models.EmailField(max_length=254)),
                ('characteristics', models.TextField()),
                ('memory', models.IntegerField()),
                ('komp', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reste.product')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnfl', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('passport_number', models.IntegerField()),
                ('issued', models.CharField(max_length=100)),
                ('date_give', models.DateTimeField(auto_now_add=True)),
                ('goden_about', models.DateTimeField(auto_now_add=True)),
                ('nationality', models.CharField(max_length=100)),
                ('citizienship', models.CharField(max_length=100)),
                ('whos_addres', models.CharField(max_length=100)),
                ('whos_number', models.CharField(max_length=100)),
                ('number_card', models.IntegerField()),
                ('term_card', models.IntegerField()),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reste.merchant')),
            ],
        ),
        migrations.CreateModel(
            name='Chooses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.BigIntegerField()),
                ('credit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reste.credit')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reste.merchant')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reste.product')),
            ],
        ),
        migrations.CreateModel(
            name='Buys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[(3, 3), (4, 4), (6, 6)], max_length=100)),
                ('date', models.DateTimeField()),
                ('payment', models.FloatField()),
                ('chooses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reste.chooses')),
                ('credit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reste.credit')),
            ],
        ),
    ]
