# Generated by Django 4.0.1 on 2022-01-12 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_lesson_order_alter_course_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='order',
            field=models.IntegerField(),
        ),
    ]