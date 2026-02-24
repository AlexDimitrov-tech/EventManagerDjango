import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('price', models.DecimalField(
                    decimal_places=2,
                    default=0.0,
                    max_digits=10,
                    validators=[django.core.validators.MinValueValidator(0)],
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(blank=True, related_name='events', to='categories.category')),
                ('venue', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='events',
                    to='venues.venue',
                )),
            ],
            options={
                'ordering': ['date', 'time'],
            },
        ),
    ]
