from django.shortcuts import render, redirect
from .forms import ProductForm, CategoryForm
from .revenue_optimizer import optimizer 
from .category import make_cat
from .models import Category, Subcategory, Product, Prouduct_Price
from django.http import JsonResponse, HttpResponse

#testing
import random

# Create your views here.
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id)
    data = [{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories]

    return JsonResponse(data, safe=False)

def create_product(request):
    form = ProductForm(request.POST or None)
    categories = Category.objects.all()

    # initialize the CategoryForm with category choices
    category_form = CategoryForm(choices=[(c.id, c.name) for c in categories])

    # initialize an empty SubcategoryForm
    subcategory_form = CategoryForm()

    if request.method == 'POST':
        if form.is_valid():
            # Get input data from the form

            """
            Demand and prices get from Pang's application
            Request: category, subcategory, sales_period
            Response: {
                wtp[i]:int
                demand[i]:int
            }

            product_revenue = wtp[i]*demand[i] for i in range(len(wtp))
            prices = [i]

            """ 

            num_of_i = random.randint(1, 10)
            demand = []
            prices = []
            for i in range(num_of_i):
                demand.append(random.randint(1,10))
                prices.append(random.randint(20, 3000))

            name = form.cleaned_data['name']
            quantity_produced = form.cleaned_data["quantity_produced"]
            sales_period = form.cleaned_data["period"]
            inventory = form.cleaned_data['inventory']
            min_price = form.cleaned_data['min_price']
            max_price = form.cleaned_data['max_price']
            category_id = request.POST.get('category')
            subcategory_id = request.POST.get('subcategory')
            category = Category.objects.get(id=category_id)
            subcategory = Subcategory.objects.get(id=subcategory_id)
            user = request.user


            product = Product(name = name, quantity_produced = quantity_produced, period = sales_period, inventory= inventory, min_price=min_price, max_price = max_price, category = category, subcategory = subcategory, user=user, total_price=0)

            product.save()

            # Call the optimization function
            """
            Expected output:
            optimized_prices:number[]
            optimized_demand: number[]
            len(optimized_prices) == len(demand)
            optimized_revenue: number[]
            """
            optimal_revenue, optimal_prices, optimal_demands = optimizer(prices, demand,quantity_produced, inventory, min_price, max_price)

            bulk_create = []
            for prices, demands in zip(optimal_prices, optimal_demands):
                revenue = prices * demands
                bulk_create.append(Prouduct_Price(product = product, price = prices, demand= demands, revenue = revenue))
            Prouduct_Price.objects.bulk_create(bulk_create)

            product.total_price = optimal_revenue
            product.save()

            # Render the output view with the optimized results
            return HttpResponse("Product added,<br /><br /><a href=\'/revenue/create-product\'>Add More product.</a><br /><a href=\'/revenue/optimization\'>Check your revenue</a><br /><a href=\'/account/dashboard\'>Go to Dashboard</a>")
        elif request.is_ajax():
            # handle Ajax request for subcategories
            category_form = CategoryForm(request.POST, choices=[(c.id, c.name) for c in categories])
            if category_form.is_valid():
                category_id = category_form.cleaned_data['category']
                category = Category.objects.get(id=category_id)
                subcategories = category.subcategories.all()
                subcategory_choices = [(s.id, s.name) for s in subcategories]
                subcategory_form = CategoryForm(choices=subcategory_choices)
                # return the new subcategory form as HTML response
                html = subcategory_form.as_p()
                return JsonResponse({'success': True, 'html': html})
            else:
                # return the errors as JSON response
                errors = category_form.errors.as_json()
                return JsonResponse({'success': False, 'errors': errors})
    else:
        # initialize an empty SubcategoryForm when first loading the page
        subcategory_form = CategoryForm()

    return render(request, 'rm/create-product.html', {
        'form': form,
        'category': category_form,
        'subcategory': subcategory_form,
    })

def add_cat(request):
    category_dict = make_cat()
    #Bulk create category
    cat = []
    subcat = []
    for key in category_dict:
        category = Category(name=key)
        cat.append(category)
        for sub_key in category_dict[key]:
            if sub_key is None or sub_key == "":
                continue
            subcat.append(Subcategory(category = category, name = sub_key))

    # Category.objects.all().delete()
    # Subcategory.objects.all().delete()

    Category.objects.bulk_create(cat)
    Subcategory.objects.bulk_create(subcat)

    return redirect('home')

def revenue_optimization(request):
    user_product = {}
    products = Product.objects.filter(user = request.user)

    total_revenue = 0
    for product in products:
        product_prices = Prouduct_Price.objects.filter(product = product)
        total_revenue += product.total_price


        price = []
        demand = []
        revenue = []
        partial_revenue = 0
        for prices in product_prices:
            price.append(prices.price)
            demand.append(prices.demand)
            revenue.append(prices.revenue)
            partial_revenue += prices.revenue

        user_product[product.name] = {
            "partial_revenue":partial_revenue,
            "revenue":[(r, p, d) for r, p, d in zip(revenue, price, demand)]
        }

    context = {
        "total_revenue":total_revenue,
        "user_product":user_product
    }
    
    return render(request, "rm/optimizer/revenue-optimization.html", context=context)
