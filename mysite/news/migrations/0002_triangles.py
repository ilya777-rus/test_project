# Generated by Django 4.1.3 on 2023-05-11 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Triangles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "vertex1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="triangles_vertex1",
                        to="news.point",
                    ),
                ),
                (
                    "vertex2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="triangles_vertex2",
                        to="news.point",
                    ),
                ),
                (
                    "vertex3",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="triangles_vertex3",
                        to="news.point",
                    ),
                ),
            ],
        ),
    ]
