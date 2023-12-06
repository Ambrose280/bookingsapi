from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('stripeproducts/', views.stripe_products, name= "setupintents"),
    path('stripeproduct/<int:pk>', views.stripe_product_detail, name='setupintent'),


    path('stripesetupintents/', views.setupintent, name= "setupintents"),
    path('stripesetupintent/<int:pk>', views.setupintent_detail, name='setupintent'),

    path('stripepaymentintents/', views.payment_intents, name= "setupintents"),
    path('stripepaymentintent/<int:pk>', views.payment_intent, name='setupintent'),

    path('striperefunditems/', views.refunditems, name= "refunditems"),
    path('striperefunditem/<int:pk>', views.refunditem, name='refunditem'),

    path('paymentmethods/', views.paymentmethods, name= "refunditems"),
    path('paymentmethod/<int:pk>', views.paymentmethod, name='refunditem'),

    path('stripesubscriptions/', views.subscriptionitems, name= "subscriptionitems"),
    path('stripesubscription/<int:pk>', views.subscriptionitem, name='subscriptionitem'),

    path('stripesessions/', views.sessionlist, name= "sessions"),
    path('stripesessiondetail/<int:pk>', views.session_detail, name='sessiondetail'),

    path('stripeplans/', views.plan, name= "plans"),
    path('stripeplandetail/<int:pk>', views.plan_detail, name='plandetail'),

    path('stripeprices/', views.stripe_prices, name= "stripeprices"),
    path('stripeprice/<int:pk>', views.stripe_price_detail, name='stripeprice'),


    path('bookings/', views.booking_list, name= "bookings"),
    path('booking/<int:pk>', views.booking_details, name='booking_detail'),

    path('users/', views.user_list, name= "user_list"),
    path('userdetails/<int:pk>', views.user_detail, name='user_detail'),
    
    path('payments/', views.paymentmethods_list, name='payments'),
    path('paymentdetail/<int:pk>', views.paymentmethods_detail, name='paymentdetail'),

    path('bookingschedules/', views.booking_schedules, name='booking_schedules'),
    path('bookingschedule/<int:pk>', views.booking_schedules_detail, name='booking_schedule'),

    path('bookingreviews/', views.reviews, name='course_modules'),
    path('bookingreview/<int:pk>', views.review_detail, name='course_module'),
    ]
    
