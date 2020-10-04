# Generated by Django 3.0 on 2020-10-03 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=264)),
                ('main_image', models.ImageField(upload_to='ItemImage')),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('discount_price', models.FloatField(default=0.0)),
                ('label', models.CharField(choices=[('N', 'New'), ('BS', 'Best Seller')], max_length=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='Store.Category')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]