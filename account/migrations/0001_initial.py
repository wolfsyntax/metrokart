# Generated by Django 2.2.1 on 2019-10-08 03:25

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
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=100)),
                ('payment_name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'PaymentMethod',
            },
        ),
        migrations.CreateModel(
            name='UserVoucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_code', models.CharField(max_length=15)),
                ('used_voucher', models.BooleanField(blank=True, null=True)),
                ('expired_voucher', models.BooleanField(blank=True, null=True)),
                ('valid_voucher', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Voucher',
                'verbose_name_plural': 'User Voucher',
                'db_table': 'user_voucher',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=13)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('C', 'Custom')], max_length=1)),
                ('birthdate', models.DateField()),
                ('loyalty_point', models.FloatField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Account',
                'verbose_name_plural': 'Customers Account',
                'db_table': 'auth_user_profile',
            },
        ),
        migrations.CreateModel(
            name='RoyaltyBonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transact_date', models.DateTimeField(auto_now_add=True)),
                ('coin_earn', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Royalty Bonus',
                'db_table': 'royalty_bonus',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consignee', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=13)),
                ('landmark', models.CharField(max_length=100)),
                ('detailed_address', models.CharField(max_length=100)),
                ('barangay', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=4)),
                ('address_type', models.CharField(choices=[('B', 'Billing Address'), ('S', 'Shipping Address')], max_length=1)),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Customers Address',
                'db_table': 'address',
            },
        ),
    ]
