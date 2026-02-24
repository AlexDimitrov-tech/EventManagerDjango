from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.CharField(
                choices=[
                    ('draft', 'Draft'),
                    ('published', 'Published'),
                    ('cancelled', 'Cancelled'),
                    ('sold_out', 'Sold Out'),
                ],
                default='draft',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='event',
            name='max_attendees',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                help_text='Leave blank for unlimited capacity.',
            ),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.UniqueConstraint(
                fields=['venue', 'date', 'time'],
                name='unique_event_slot_per_venue',
            ),
        ),
    ]

