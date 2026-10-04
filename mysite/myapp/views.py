from datetime import datetime
from django.db.models  import Q
from itertools import product
from django.db.models import Sum
from django.shortcuts import render,redirect
from .models import Product, OrderDetail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.http import JsonResponse
from .forms import ProductForm,UserRegistrationForm
from . import models
from django.db.models import Sum
import datetime




def index(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    products = Product.objects.all()

    # Hide logged-in user's own products
    if request.user.is_authenticated:
        products = products.exclude(seller=request.user)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category:
        products = products.filter(category=category)

    return render(
        request,
        'myapp/index.html',
        {
            'products': products,
            'query': query,
            'category': category
        }
    )
    # products = Product.objects.all()

    # return render(
    #     request,
    #     'myapp/index.html',
    #     {'products': products}
    # )


def detail(request, id):

    product = Product.objects.get(id=id)

    razorpay_publishable_key = settings.RAZORPAY_KEY_ID

    return render(
        request,
        'myapp/detail.html',
        {
            'product': product,
            'razorpay_publishable_key': razorpay_publishable_key
        }
    )


@csrf_exempt
def create_checkout_order(request, id):

    # Get product
    product = Product.objects.get(id=id)

     # Seller cannot buy their own product
    if product.seller == request.user:
        return redirect('invalid')




    # Connect to Razorpay
    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    # Convert price to paise
    amount = int(product.price * 100)

    # Create Razorpay order
    order = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': 1
    })

    # Create our Django order
    order_detail = OrderDetail()
    order_detail.customer_email = request.user.email

    order_detail.product = product
    order_detail.amount = int(product.price)
    order_detail.has_paid = False

    order_detail.save()

    # Open checkout page
    return render(
        request,
        'myapp/checkout.html',
        {
            'product': product,
            'razorpay_order_id': order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount,
            'order_detail_id': order_detail.id
        }
    )


@csrf_exempt
def payment_success(request):

    payment_id = request.POST.get('razorpay_payment_id')

    razorpay_order_id = request.POST.get(
        'razorpay_order_id'
    )

    signature = request.POST.get(
        'razorpay_signature'
    )

    order_detail_id = request.POST.get(
        'order_detail_id'
    )

    # Connect to Razorpay
    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:

        # Verify payment
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        # Find our Django order
        order_detail = OrderDetail.objects.get(
            id=order_detail_id
        )

        # Update payment information
        order_detail.razorpay_payment_id = payment_id
        order_detail.has_paid = True

        # updating sales stats for product
        product = Product.objects.get(id= order_detail.product.id)
        
        product.total_sales_amount += int(product.price)
        product.total_sales += 1
        # updating sales stats for product
        product.save()

        order_detail.save()
        return JsonResponse({
            'success': True
        })

    except Exception:

        return JsonResponse(
            {
                'error': 'Payment verification failed'
            },
            status=400
        )

def success(request):
    return render(request, 'myapp/success.html')

def fail(request):
    return render(request,'myapp/fail.html')


def create_product(request):
    product_form = ProductForm()
    if request.method == "POST":
       product_form = ProductForm(request.POST, request.FILES)
       if product_form.is_valid():
           new_product = product_form.save(commit=False)
           new_product.seller = request.user
           new_product.save()
           return redirect('index')
    return render(request,'myapp/create_product.html',{'product_form':product_form})


def product_edit(request , id):
    product = Product.objects.get(id=id)
    if product.seller != request.user:
        return redirect('invalid')
    product_form = ProductForm(request.POST or None, request.FILES or None , instance=product) 
    if request.method == "POST" :
        if product_form.is_valid():
            product_form.save()
            return redirect('index')
    return render(request,'myapp/product_edit.html',{'product_form':product_form,'product':product})


def product_delete(request,id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.delete()
        return redirect('index')
    return render(request,'myapp/delete.html',{'product':product})

from django.db.models import Sum

def dashboard(request):
    products = Product.objects.filter(seller=request.user)

    total_orders = OrderDetail.objects.filter(
        product__in=products,
        has_paid=True
    ).count()

    total_earnings = OrderDetail.objects.filter(
        product__in=products,
        has_paid=True
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(
        request,
        'myapp/dashboard.html',
        {
            'products': products,
            'total_orders': total_orders,
            'total_earnings': total_earnings,
        }
    )

def register(request):

    user_form = UserRegistrationForm()

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data['password1']
            )

            new_user.save()

            return redirect('index')

    return render(
        request,
        'myapp/register.html',
        {'user_form': user_form}
    )

def invalid(request):
    return render(request,'myapp/invalid.html')

def my_purchases(request):
    orders = OrderDetail.objects.filter(customer_email = request.user.email,has_paid = True)
    return render(request,'myapp/purchases.html',{'orders':orders})


def sales(request):
    orders = OrderDetail.objects.filter(product__seller=request.user,has_paid=True)
    total_sales = orders.aggregate(total=Sum('amount'))['total'] or 0

    #Logic to calculate 365 days expenses

    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = OrderDetail.objects.filter(created_on__gt=last_year,product__seller=request.user)
    yearly_sum = data.aggregate(Sum('amount'))['amount__sum']


    #Monthly sum
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = OrderDetail.objects.filter(created_on__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))['amount__sum']

    #Weekly sum
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = OrderDetail.objects.filter(created_on__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))['amount__sum']

#everyday sum  for  past 30 days
    daily_sales_sums =OrderDetail.objects.filter(product__seller = request.user).values('created_on__date').order_by('created_on__date').annotate(sum=Sum('amount'))
    # print(daily_sales_sums)

    product_sales_sums = OrderDetail.objects.filter(product__seller = request.user).values('product__name').order_by('product__name').annotate(sum=Sum('amount'))

    print(product_sales_sums)
    
    return render(request,'myapp/sales.html',{'orders':orders,'total_sales':total_sales,'yearly_sum':yearly_sum,'monthly_sum':monthly_sum,'weekly_sum':weekly_sum,'daily_sales_sums':daily_sales_sums,'product_sales_sums':product_sales_sums})
    all_amount = OrderDetail.objects.filter(product__seller=request.user,has_paid=True)

def orders(request):

    # All paid orders for products sold by the logged-in seller
    orders = OrderDetail.objects.filter(
        product__seller=request.user,
        has_paid=True
    ).order_by('-created_on')

    # Paid orders received today
    date_of_received = OrderDetail.objects.filter(
        product__seller=request.user,
        has_paid=True,
        created_on__date=datetime.date.today()
    ).order_by('-created_on')

    return render(
        request,
        'myapp/orders.html',
        {
            'orders': orders,
            'date_of_received': date_of_received
        }
    )