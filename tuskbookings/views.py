from django.shortcuts import render

# Create your views here.
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth.models import User
import stripe
from dotenv import load_dotenv
import os
from djstripe.models import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def endpoints(request):
    data = ['Booking API']
    return Response(data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def plan(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        plans = Plan.objects.filter(Q(id__icontains=query))
        serializer = PriceSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.Plan.create(amount=request.data["amount"], currency=request.data["currency"], interval="month", product = request.data["product"],)
            return Response(prod, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def plan_detail(request, pk):
    try:
        plan = Plan.objects.get(pk=pk)
    except Plan.DoesNotExist:
        return Response({"detail": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlanSerializer(plan, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = PlanSerializer(plan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        plan.delete()
        return Response({"detail": "Plan deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def stripe_prices(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        prices = Price.objects.filter(Q(id__icontains=query))
        serializer = PriceSerializer(prices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.Product.create(unit_amount=request.data["unit_amount"], currency=request.data["currency"], product=request.data["product"], recurring={"interval": "month"},)
            return Response(prod, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def stripe_price_detail(request, pk):
    try:
        price = Price.objects.get(pk=pk)
    except Price.DoesNotExist:
        return Response({"detail": "Price not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PriceSerializer(price, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = PriceSerializer(price, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        price.delete()
        return Response({"detail": "Price deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sessionlist(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        sessions = Session.objects.filter(Q(id__icontains=query))
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.financial_connections.Session.create(account_holder={"type": "customer", "customer": request.data['customer'],}, 
                                                               permissions=["payment_method", "balances"], filters={"countries": [request.data['country']]},)
            return Response(prod, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def session_detail(request, pk):
    try:
        session = Session.objects.get(pk=pk)
    except Session.DoesNotExist:
        return Response({"detail": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SessionSerializer(session, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = SessionSerializer(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        plan.delete()
        return Response({"detail": "Session deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def subscriptionitems(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        subscriptionitems = Subscription.objects.filter(Q(id__icontains=query))
        serializer = SubscriptionSerializer(subscriptionitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.Subscription.create(customer= request.data['customer'], 
            items=[{"price": request.data['price']},],)
            return Response(prod, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscriptionitem(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        return Response({"detail": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubscriptionSerializer(subscriptionitem, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = SubscriptionSerializer(subscriptionitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        subscription.delete()
        return Response({"detail": "Subscription deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def paymentmethods(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        paymentmethods = PaymentMethod.objects.filter(Q(id__icontains=query))
        serializer = PaymentMethodSerializer(paymentmethods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.PaymentMethod.create(type="card", card={"number": request.data['number'], "exp_month": request.data['exp_month'], "exp_year": request.data['exp_year'], "cvc": request.data['cvc'],},)
            return Response(prod, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def paymentmethod(request, pk):
    try:
        paymentmethod = PaymentMethod.objects.get(pk=pk)
    except PaymentMethod.DoesNotExist:
        return Response({"detail": "Payment Method not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PaymentMethodSerializer(paymentmethod, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = PaymentMethodSerializer(paymentmethod, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        paymentmethod.delete()
        return Response({"detail": "Payment Method deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def refunditems(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        refunditems = Refund.objects.filter(Q(id__icontains=query))
        serializer = RefundSerializer(refunditems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.Refund.create(charge= request.data['charge'])
            return Response(prod, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def refunditem(request, pk):
    try:
        refunditem = Refund.objects.get(pk=pk)
    except Refund.DoesNotExist:
        return Response({"detail": "Refund not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RefundSerializer(refunditem, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = RefundSerializer(refunditem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        refunditem.delete()
        return Response({"detail": "Refund deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def setupintent(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        setup_intent = SetupIntent.objects.filter(Q(id__icontains=query))
        serializer = SetupIntentSerializer(setup_intent, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.SetupIntent.create(automatic_payment_methods={"enabled": True},)
            return Response(prod, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def setupintent_detail(request, pk):
    try:
        setupintent = InvoiceItem.objects.get(pk=pk)
    except InvoiceItem.DoesNotExist:
        return Response({"detail": "Setup Intent not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SetupIntentSerializer(setupintent, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = SetupIntentSerializer(setupintent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        setupintent.delete()
        return Response({"detail": "Setup Intent deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def invoice_items(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        invoice_item = InvoiceItem.objects.filter(Q(id__icontains=query))
        serializer = InvoiceItemSerializer(invoice_item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.SetupIntent.create(automatic_payment_methods={"enabled": True},)
            return Response(prod, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def invoice_item(request, pk):
    try:
        invoice_item = InvoiceItem.objects.get(pk=pk)
    except InvoiceItem.DoesNotExist:
        return Response({"detail": "Invoice Item not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InvoiceItemSerializer(invoice_item, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = InvoiceItemSerializer(invoice_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        invoice_item.delete()
        return Response({"detail": "Invoice Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def payment_intents(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        payment_item = PaymentIntent.objects.filter(Q(id__icontains=query))
        serializer = PaymentIntentSerializer(payment_item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.PaymentIntent.create(amount= request.data['amount'], currency= request.data['currency'], automatic_payment_methods={"enabled": True})
            return Response(prod, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def payment_intent(request, pk):
    try:
        paymentitem = PaymentIntent.objects.get(pk=pk)
    except PaymentIntent.DoesNotExist:
        return Response({"detail": "Payment Intent not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PaymentIntentSerializer(paymentitem, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = PaymentIntentSerializer(paymentitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        paymentitem.delete()
        return Response({"detail": "Payment Intent deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def payout_items(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        payment_item = Payout.objects.filter(Q(id__icontains=query))
        serializer = PayoutSerializer(payment_item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.PaymentIntent.create(amount= request.data['amount'], currency= request.data['currency'])
            return Response(prod, status=status.HTTP_200_OK)
        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def payout_item(request, pk):
    try:
        paymentitem = Payout.objects.get(pk=pk)
    except Payout.DoesNotExist:
        return Response({"detail": "Payout not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PayoutSerializer(paymentitem, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = PayoutSerializer(paymentitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        paymentitem.delete()
        return Response({"detail": "Payout Log deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def stripe_products(request):
    stripe.api_key = os.environ.get('STRIPE_TEST_SECRET_KEY')
    if request.method == 'GET':
        query = request.GET.get('query', '')
        # Use Q objects to perform a case-insensitive search in title and description fields
        prods = Product.objects.filter(Q(description__icontains=query))
        serializer = ProductSerializer(prods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.Product.create(name=request.data["name"], description=request.data["description"])

            return Response(prod, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            # Handle other exceptions
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def subscriptions(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        subscriptionitems = Subscription.objects.filter(Q(id__icontains=query))
        serializer = SubscriptionSerializer(subscriptionitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.Product.create(customer=request.data["customer"], items=[{"price": request.data["price"]},],)

            return Response(prod, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            # Handle other exceptions
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def discount(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        discount = Discount.objects.filter(Q(id__icontains=query))
        serializer = DiscountSerializer(discount, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        try:
            prod = stripe.Product.create(name=request.data["name"], description=request.data["description"])

            return Response(prod, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({"Fortune, work smarter": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            # Handle other exceptions
            return Response({"Fortune, work smarter": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def discount_detail(request, pk):
    try:
        discount_detail = Discount.objects.get(pk=pk)
    except Discount.DoesNotExist:
        return Response({"detail": "Discount not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DiscountSerializer(discount_detail, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = DiscountSerializer(discount_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        discount_detail.delete()
        return Response({"detail": "Discount deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscription(request, pk):
    try:
        subscriptionitem = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        return Response({"detail": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubscriptionSerializer(subscriptionitem, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = SubscriptionSerializer(subscriptionitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        subscriptionitem.delete()
        return Response({"detail": "Subscription deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        

    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def stripe_product_detail(request, pk):
    try:
        prods = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"detail": "Stripe Product not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(prods, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = ProductSerializer(prods, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        prods.delete()
        return Response({"detail": "Stripe Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_list(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        booking = User.objects.filter(Q(username__icontains=query) | Q(username__icontains=query))
        serializer = UserSerializers(booking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        booking_detail = User.objects.get(pk=pk)
    except BookingService.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializers(booking_detail, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = UserSerializers(booking_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        booking_detail.delete()
        return Response({"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking_list(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        booking = BookingService.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def booking_details(request, pk):
    try:
        booking_detail = BookingService.objects.get(pk=pk)
    except BookingService.DoesNotExist:
        return Response({"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookingSerializer(booking_detail, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = BookingSerializer(booking_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        booking_detail.delete()
        return Response({"detail": "Booking deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def paymentmethods_list(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        payment_method = PaymentMethod.objects.filter(Q(method__icontains=query))
        serializer = PaymentMethodSerializer(payment_method, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def paymentmethods_detail(request, pk):
    try:
        payment_method_detail = PaymentMethod.objects.get(pk=pk)
    except PaymentMethod.DoesNotExist:
        return Response({"detail": "Payment method not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PaymentMethodSerializer(payment_method_detail, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = PaymentMethodSerializer(payment_method_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        payment_method_detail.delete()
        return Response({"detail": "Payment method deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking_schedules(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        booking_schedule = BookingSchedule.objects.filter(Q(end_date__icontains=query))
        serializer = BookingScheduleSerializer(booking_schedule, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = BookingScheduleSerializer(data=request.data)
        data = request.POST
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def booking_schedules_detail(request, pk):
    try:
        booking_schedules_detail = BookingSchedule.objects.get(pk=pk)
    except PaymentMethod.DoesNotExist:
        return Response({"detail": "Booking Schedule not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookingScheduleSerializer(booking_schedules_detail, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = BookingScheduleSerializer(booking_schedules_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        booking_schedules_detail.delete()
        return Response({"detail": "Booking Schedule succesfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    

    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reviews(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        # Use Q objects to perform a case-insensitive search in title and description fields
        reviews = Review.objects.filter(Q(rating__icontains=query))
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_detail(request, pk):
    try:
        review_detail = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response({"detail": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review_detail, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = ReviewSerializer(review_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        review_detail.delete()
        return Response({"detail": "Review log not found"}, status=status.HTTP_204_NO_CONTENT)
    