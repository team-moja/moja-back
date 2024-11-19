# Generated by Django 4.2.16 on 2024-11-19 08:09

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
            name='HelpArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_title', models.CharField(max_length=255, verbose_name='질문 제목')),
                ('help_content', models.TextField(verbose_name='질문 내용')),
                ('help_date', models.DateField(auto_now_add=True, verbose_name='질문 작성일')),
                ('help_delete_date', models.DateField(blank=True, null=True, verbose_name='삭제일')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
        ),
        migrations.CreateModel(
            name='HelpComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_comment_content', models.TextField(verbose_name='댓글 내용')),
                ('help_comment_date', models.DateField(auto_now_add=True, verbose_name='작성일')),
                ('help_comment_delete_date', models.DateField(blank=True, null=True, verbose_name='삭제일')),
                ('help_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.helparticle', verbose_name='관련 질문')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
        ),
        migrations.CreateModel(
            name='HelpLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.helparticle', verbose_name='좋아요한 질문')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='좋아요한 회원')),
            ],
            options={
                'unique_together': {('user', 'help_article')},
            },
        ),
    ]
