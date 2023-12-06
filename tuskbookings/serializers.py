from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

from djstripe.models import *


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class DiscountSerializer(ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceItemSerializer(ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'

class SubscriptionItemSerializer(ModelSerializer):
    class Meta:
        model = SubscriptionItem
        fields = '__all__'

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class PaymentIntentSerializer(ModelSerializer):
    class Meta:
        model = PaymentIntent
        fields = '__all__'

class PayoutSerializer(ModelSerializer):
    class Meta:
        model = Payout
        fields = '__all__'

class SetupIntentSerializer(ModelSerializer):
    class Meta:
        model = SetupIntent
        fields = '__all__'

class RefundSerializer(ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'

class PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class SubscriptionScheduleSerializer(ModelSerializer):
    class Meta:
        model = SubscriptionSchedule
        fields = '__all__'

class SessionSerializer(ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class PlanSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class PriceSerializer(ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ActiveHoursSerializer(ModelSerializer):
    class Meta:
        model = ActiveHours
        fields = '__all__'
       

class BookingSerializer(ModelSerializer):
    class Meta:
        model = BookingService
        fields = '__all__'
   

class BookingScheduleSerializer(ModelSerializer):

    
    class Meta:

        model = BookingSchedule
        fields = '__all__'
    

class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
       








