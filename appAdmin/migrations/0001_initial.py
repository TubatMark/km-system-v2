# Generated by Django 4.2.7 on 2025-03-13 05:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('about_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'tbl_about',
            },
        ),
        migrations.CreateModel(
            name='AboutFooter',
            fields=[
                ('about_footer_id', models.AutoField(primary_key=True, serialize=False)),
                ('content_footer', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'tbl_about_footer',
            },
        ),
        migrations.CreateModel(
            name='CMI',
            fields=[
                ('cmi_id', models.AutoField(primary_key=True, serialize=False)),
                ('cmi_name', models.CharField(max_length=255)),
                ('cmi_meaning', models.CharField(max_length=255)),
                ('cmi_description', models.TextField()),
                ('address', models.CharField(max_length=255, null=True)),
                ('contact_num', models.CharField(max_length=20, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('cmi_image', models.ImageField(null=True, upload_to='cmi/')),
                ('status', models.CharField(default='Approved', max_length=255)),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('url', models.URLField(null=True)),
                ('date_joined', models.DateField(null=True)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'tbl_cmi',
            },
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('commodity_id', models.AutoField(primary_key=True, serialize=False)),
                ('commodity_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('resources_type', models.CharField(max_length=100)),
                ('commodity_img', models.ImageField(null=True, upload_to='commodities/')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('date_edited', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(default='Approved', max_length=255)),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
            ],
            options={
                'db_table': 'tbl_commodity',
            },
        ),
        migrations.CreateModel(
            name='KnowledgeResources',
            fields=[
                ('knowledge_id', models.AutoField(primary_key=True, serialize=False)),
                ('knowledge_title', models.CharField(max_length=255)),
                ('knowledge_description', models.TextField()),
                ('status', models.CharField(default='Approved', max_length=255)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
            options={
                'db_table': 'tbl_knowledge',
            },
        ),
        migrations.CreateModel(
            name='UsefulLinks',
            fields=[
                ('link_id', models.AutoField(primary_key=True, serialize=False)),
                ('link_title', models.CharField(max_length=255, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('status', models.CharField(default='Approved', max_length=255)),
                ('date_created', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'tbl_useful_links',
            },
        ),
    ]
