from django.contrib import admin
from .models import *
import admin_thumbnails
from django.contrib.admin.sites import AdminSite

from django.contrib.admin.sites import AdminSite

from .models import *

import admin_thumbnails


AdminSite.site_header = "WebTusk Administration"
AdminSite.site_title = "WebTusk Administration"

AdminSite.index_title = "Authorized Personnel Only"

@admin_thumbnails.thumbnail('booking_image')
class BookingAdmin(admin.ModelAdmin):
    
    list_display = ('created_by', 'title', 'tagline', 'booking_image_thumbnail', 'recurring_payment', 'onetime_payment', 'price', 'calculate_discounted_price')
    list_filter = ('title',)
    search_fields = ('title',)


class ActiveHoursAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'opening', 'closing', 'used_hours', 'available_days')


class ReviewAdmin(admin.ModelAdmin):
    
    list_display = ('booking', 'user', 'rating', 'comment', 'created_at')
    
class PaymentAdmin(admin.ModelAdmin):
    
    list_display = ('booking', 'user', 'amount', 'payment_date', 'payment_method')
    
class BookingScheduleAdmin(admin.ModelAdmin):
    
    list_display = ('client','booking_service', 'start_time', 'end_time', 'accepted')
    

class PaymentMethodAdmin(admin.ModelAdmin):
    
    list_display = ('method',)
    
class StaffAdmin(admin.ModelAdmin):
    
    list_display = ('staff', 'schedule')
    


# Register your models here.
admin.site.register(ActiveHours, ActiveHoursAdmin)
admin.site.register(BookingService, BookingAdmin)

admin.site.register(BookingSchedule, BookingScheduleAdmin)

admin.site.register(Review, ReviewAdmin)
admin.site.register(Staff, StaffAdmin)