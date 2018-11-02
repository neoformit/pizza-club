import os
import datetime
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from form.models import Order, Participant

# Create your views here.
def menu(request):
    def open():
        day = datetime.datetime.today().weekday()
        hour = datetime.datetime.now().hour
        if day < 4:
            return True
        elif day == 4:
            if hour < 11:
                return True
            else:
                return False
        else:
            return False
    
    if open():
        print('\nPizza line is open!')
        # default menu.html
        return render(request, 'form/menu.html')
    else:
        print('\nPizza line is closed.')
        return render(request, 'form/closed.html')

def confirm(request):
    
    price_lookup = {
                    "Vegan margherita":7.95,
                    "Vegan spicy veg trio":7.95,
                    "Spicy veg trio":5.0,
                    "Margherita":5.0,
                    "BBQ italian sausage":5.0,
                    "BBQ pork & onion":5.0,
                    "Pepperoni":5.0
    }
    
    if request.method == 'POST':
        
        # Create an instance of Order
        # request.POST will contain {'name':'John',item='Vg margherita'}
        # so must add date from datetime and price from price_lookup
        
        r = {}
        for key,value in request.POST.items():
            if key != "csrfmiddlewaretoken":
                r[key] = value
        
        try:
            r['item']
        except KeyError:
            return render(request, 'form/menu-item.html') ## error menu.html
        
        try:
            r['name']
        except KeyError:
            return render(request, 'form/menu-name.html') ## error menu.html
        
        try:
            r['crust']
        except KeyError:
            r['crust'] = "regular"
        
        print("\n## Data returned: ##")
        for key,value in r.items():
            print("%s : %s" % (key,value))
        
        r['date'] = str(datetime.date.today())
        try:
            r['cost'] = price_lookup[r['item']]
        except KeyError:
            raise KeyError("Selected item was not found in price_lookup dictionary")
            
        print("Date: %s   Cost: $%.2f" % (r['date'],r['cost']))
        
        order = Order() # Order imported from models
        order.name = r['name']
        order.date = r['date']
        order.item = r['item']
        order.cost = r['cost']
        order.crust = r['crust']
        order.comments = r['comments']
        order.save()
        
        request.session['order_id'] = order.id    # Or order.pk?
        
        with open(os.path.join(settings.MEDIA_ROOT, 'orders.txt'), 'a+') as f:
            f.write("\n%s\t%s\t%s\t%s\t%s" % (r['date'],r['name'],r['item'],r['cost'],r['crust']))
            print("Order recorded in orders.txt\n")
        
        # Redirect to confirmation page
        # return render(request, 'form/confirm.html', r) #pass dict of order details
        return redirect("/confirmation")
    
    else:
        print("Request method: %s" % request.method)
        return HttpResponse("Error! GET request received from form.")

def confirmation(request):
    # Read order from db into dictionary to render as below:
    o = Order.objects.get(id=request.session["order_id"])
    p = Participant.objects.latest("last_turn")
    return render(request, 'form/confirm.html', {'item':o.item,'crust':o.crust,'pizzaman':p.name})
    # Maybe also add in a list of current orders??

def cancel(request):
    
    ## Remove last Order from database:
    oid=request.session["order_id"]
    try:
        o = Order.objects.get(id=oid)
        o.delete()
        print("Order number %s has been deleted" % oid)
    except:
        print("Order number %s could not be deleted" % oid)
        pass
        
    def open():
        day = datetime.datetime.today().weekday()
        hour = datetime.datetime.now().hour
        if day < 4:
            return True
        elif day == 4:
            if hour < 11:
                return True
            else:
                return False
        else:
            return False
    if open():
        print('\nPizza line is open!')
        # Menu with "cancelled" modal
        return render(request, 'form/menu-cancelled.html')
    else:
        print('\nPizza line is closed.')
        return render(request, 'form/closed.html')