from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="coffee_note",
            field=models.CharField(
                blank=True,
                help_text="ör. Etkinlik sonrası V60 demleme ikramı",
                max_length=200,
                verbose_name="Kahve ikramı",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="activity_type",
            field=models.CharField(
                choices=[
                    ("run", "Koşu"),
                    ("yoga", "Yoga & Pilates"),
                    ("hike", "Doğa Yürüyüşü"),
                    ("bike", "Bisiklet"),
                ],
                default="run",
                max_length=20,
                verbose_name="Aktivite türü",
            ),
        ),
    ]
