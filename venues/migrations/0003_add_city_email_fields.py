from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venues', '0002_venue_phone_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='city',
            field=models.CharField(default='Unknown', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.RemoveField(
            model_name='venue',
            name='website',
        ),
        migrations.RemoveConstraint(
            model_name='venue',
            name='venue_capacity_positive',
        ),
    ]
