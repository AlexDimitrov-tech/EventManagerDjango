from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='venue',
            name='website',
            field=models.URLField(blank=True),
        ),
        migrations.AddConstraint(
            model_name='venue',
            constraint=models.CheckConstraint(
                condition=models.Q(capacity__gte=1),
                name='venue_capacity_positive',
            ),
        ),
    ]

