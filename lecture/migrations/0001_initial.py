# Generated by Django 4.2.11 on 2032-12-16 00:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import lecture.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer_View',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme', models.CharField(choices=[('Select Programme', 'Select Programme'), ('Bsc', 'Bsc'), ('CEP', 'CEP'), ('Masters', 'Masters'), ('PhD', 'PhD'), ('Sandwich', 'Sandwich')], default='Select Programme', max_length=100)),
                ('year', models.CharField(choices=[('Select Year', 'Select Year'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], default='Select Year', max_length=100)),
                ('task', models.CharField(choices=[('Select Task', 'Select Task'), ('Assignment', 'Assignment'), ('Handout', 'Handout'), ('Quiz', 'Quiz'), ('Pin', 'Pin')], default='Select Task', max_length=100)),
                ('upload', models.FileField(blank=True, upload_to='docs/', validators=[lecture.validators.result_file])),
                ('number_of_student', models.IntegerField(blank=True, default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Scratch_Pin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme', models.CharField(choices=[('Select Programme', 'Select Programme'), ('Bsc', 'Bsc'), ('CEP', 'CEP'), ('Masters', 'Masters'), ('PhD', 'PhD'), ('Sandwich', 'Sandwich')], default='Select Programme', max_length=100)),
                ('year', models.CharField(choices=[('Select Year', 'Select Year'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], default='Select Year', max_length=100)),
                ('task', models.CharField(choices=[('Select Task', 'Select Task'), ('Assignment', 'Assignment'), ('Handout', 'Handout'), ('Quiz', 'Quiz'), ('Pin', 'Pin')], default='Select Task', max_length=100)),
                ('student_reg', models.IntegerField(blank=True, default=0)),
                ('number', models.IntegerField(blank=True, default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz_Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('reg_number', models.IntegerField()),
                ('quiz_upload', models.FileField(upload_to='docs/', validators=[lecture.validators.result_file])),
                ('score', models.IntegerField(blank=True, default=0)),
                ('is_opened', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.lecturer_view')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pics', models.ImageField(blank=True, upload_to='Pictures/')),
                ('phone', models.IntegerField(default=0)),
                ('degree', models.CharField(choices=[('Select Position', 'Select Position'), ('Bsc', 'Bsc'), ('Masters', 'Masters'), ('PhD', 'PhD')], default='Select Position', max_length=100)),
                ('gender', models.CharField(choices=[('Select Gender', 'Select Gender'), ('Female', 'Female'), ('Male', 'Male')], default='Select Gender', max_length=100)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment_Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('reg_number', models.IntegerField()),
                ('ass_upload', models.FileField(upload_to='docs/', validators=[lecture.validators.result_file])),
                ('score', models.IntegerField(blank=True, default=0)),
                ('is_opened', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.lecturer_view')),
            ],
        ),
    ]
