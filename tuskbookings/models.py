from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, timezone
import stripe

class ActiveHours(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opening = models.DateTimeField()
    closing = models.DateTimeField(null=True)

    def available_days(self): 
        start = self.opening
        end = self.closing
        total = end - start
        return total




    def parse_datetime(dt_str):
        return datetime.strptime(dt_str, "datetime.datetime(%Y, %m, %d, %H, %M, tzinfo=datetime.timezone.utc)")
    
    def used_hours(self): 
        services_by_user = BookingService.objects.filter(created_by_id = self.user.id).values()
        #getting the IDs of the services made by created by a user
        id_list = [item['id'] for item in services_by_user]
        schedules = BookingSchedule.objects.all().values()
        # gets all schedules
        service_ids = id_list
        output_ = [item for item in schedules if item['booking_service_id'] in service_ids]
        data = output_
        total_time_difference_minutes = 0
        for item in output_:
            start_time = item['start_time']
            end_time = item['end_time']
            time_difference = end_time - start_time
            time_difference_minutes = time_difference.total_seconds() / 60
            total_time_difference_minutes += time_difference_minutes
        total_time_difference_hours = total_time_difference_minutes / 60
        tp = self.available_days()
        
        return total_time_difference_hours, "Hours"

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name_plural = 'Active Hours'





class BookingService(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    active_hours = models.ForeignKey(ActiveHours, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, default="__")
    description = models.TextField(max_length=256, default="__")
    tagline = models.TextField(max_length=256, default="__")
    booking_image = models.ImageField(upload_to='bookingimgs', blank=True, null=True, verbose_name="Course Image", default='bookingimgs/9966d98ae582de37ed2f4d56c557d6d4_S93cfX7.jpg')
    registered_users = models.ManyToManyField(User, related_name='registered_bookings', blank=True)
    recurring_payment = models.BooleanField(default=False)
    onetime_payment = models.BooleanField(default=False)
    meeting_url = models.URLField(max_length=200, blank=True, null=True)  # Added missing field name
    color = models.TextField(max_length=500, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    has_discount = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.id:
            try:
                product = stripe.Product.create(
                    name=self.title,
                    description=self.description,)
            except stripe.error.StripeError as e:
                raise ValidationError('Invalid Input Fed')
        super().save(*args, **kwargs)
    
    def calculate_discounted_price(self):
        if self.has_discount:
            discount_amount = self.price * (self.discount_percentage / 100)
            discounted_price = self.price - discount_amount
            return discounted_price
        return self.price

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Booking Services'
        verbose_name = 'Booking Services'
#Rolled Back Code



    

def parse_datetime(dt_str):
    return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')

def check_conflict(durations):
    for i, duration in enumerate(durations):
        start1, end1 = duration
        for j, other_duration in enumerate(durations):
            if i != j:  # Don't compare the same duration
                start2, end2 = other_duration
                if start1 <= end2 and end1 >= start2:
                    return True  # Conflicting durations found
    return False  # No conflicts found
#finalised code confilcts

class BookingSchedule(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    booking_service = models.ForeignKey(BookingService, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    accepted = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = 'Booking Schedules'
        verbose_name = 'Booking Schedule'
    
     


        

    def save(self, *args, **kwargs):
        if self.booking_service and self.booking_service.active_hours:
            availability = self.booking_service.active_hours
            if self.start_time < availability.opening or self.end_time > availability.closing:
                raise ValidationError("Booking schedule mismatches the active hours of the associated service provider")
            if 1 > 0:
                time_list = []
                data = BookingSchedule.objects.all().values()

                for entry in data:
                    start = entry['start_time']
                    end = entry['end_time']
                    start_time = start.strftime('%Y-%m-%d %H:%M:%S')
                    end_time = end.strftime('%Y-%m-%d %H:%M:%S')
                    time_list.append([start_time, end_time])
                    parsed_durations = [(parse_datetime(start), parse_datetime(end)) for start, end in time_list]
                    conflict = check_conflict(parsed_durations)
                    if conflict:
                        raise ValidationError("There are conflicting datetime durations.")
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.booking_service.title}"
    
    

    



    

class Review(models.Model):
    booking = models.ForeignKey(BookingService, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

class Staff(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(BookingSchedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff.username
    class Meta:
        verbose_name_plural="Staff"

