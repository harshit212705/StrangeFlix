# Generated by Django 3.1.2 on 2020-10-04 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20201004_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, default='', max_length=100)),
                ('transaction_end_time', models.DateTimeField(auto_now_add=True)),
                ('transaction_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transaction.transactiondetails')),
            ],
            options={
                'verbose_name_plural': 'Transaction Tokens',
            },
        ),
    ]
