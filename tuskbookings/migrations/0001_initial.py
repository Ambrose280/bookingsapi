# Generated by Django 4.2.4 on 2023-09-01 09:08

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
            name='ActiveHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening', models.DateTimeField()),
                ('closing', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Active Hours',
            },
        ),
        migrations.CreateModel(
            name='BookingSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Booking Schedule',
                'verbose_name_plural': 'Booking Schedules',
            },
        ),
        migrations.CreateModel(
            name='BookingService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='__', max_length=200)),
                ('description', models.TextField(default='__', max_length=256)),
                ('tagline', models.TextField(default='__', max_length=256)),
                ('booking_image', models.ImageField(blank=True, default='bookingimgs/9966d98ae582de37ed2f4d56c557d6d4_S93cfX7.jpg', null=True, upload_to='bookingimgs', verbose_name='Course Image')),
                ('recurring_payment', models.BooleanField(default=False)),
                ('onetime_payment', models.BooleanField(default=False)),
                ('meeting_url', models.URLField(blank=True, null=True)),
                ('color', models.TextField(max_length=500, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('has_discount', models.BooleanField(default=False)),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('active_hours', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tuskbookings.activehours')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('registered_users', models.ManyToManyField(blank=True, related_name='registered_bookings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Booking Services',
                'verbose_name_plural': 'Booking Services',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('Stripe', 'Stripe'), ('Paypal', 'Paypal')], default='Stripe', max_length=50)),
            ],
            options={
                'verbose_name': 'Payment Method',
                'verbose_name_plural': 'Payment Methods',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tuskbookings.bookingschedule')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Staff',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tuskbookings.bookingservice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tuskbookings.bookingservice')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tuskbookings.paymentmethod')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bookingschedule',
            name='booking_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tuskbookings.bookingservice'),
        ),
        migrations.AddField(
            model_name='bookingschedule',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
