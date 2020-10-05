# Generated by Django 3.1.2 on 2020-10-05 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0007_auto_20201005_0733'),
        ('subscribe', '0002_subscriptions'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionAdditionalTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='subscribe.subscriptions')),
                ('transaction_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transaction.transactiondetails')),
            ],
            options={
                'verbose_name_plural': 'Subscription Additional Transaction',
            },
        ),
    ]
