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
        if day < 4:                                      #!!! Change back to 11!
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
        return render(request, 'form/test.html') ## default menu.html
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
        print("\n## Data returned: ##")
        for key,value in r.items():
            print("%s : %s" % (key,value))
        
        r['date'] = str(datetime.date.today())
        r['cost'] = price_lookup[r['item']]
        print("Date: %s   Cost: $%.2f" % (r['date'],r['cost']))
        
        order = Order() # Order imported from models
        order.name = r['name']
        order.date = r['date']
        order.item = r['item']
        order.cost = r['cost']
        order.save()
        
        request.session['order_id'] = order.id    # Or order.pk?
        
        with open(os.path.join(settings.MEDIA_ROOT, 'orders.txt'), 'a+') as f:
            f.write("\n%s\t%s\t%s\t%s" % (r['date'],r['name'],r['item'],r['cost']))
            print("Order recorded in orders.txt\n")
        
        # Redirect to confirmation page
        # return render(request, 'form/confirm.html', r) #pass dict of order details
        return redirect("/confirmation")
    
    else:
        print("Request method: %s" % request.method)
        return HttpResponse("Error! GET request received from form.")

def confirmation(request):
    # Read order from db into dictionary to render as below:
    order = Order.objects.get(id=request.session["order_id"])
    p = Participant.objects.latest("last_turn")
    return render(request, 'form/confirm.html', {'item':order.item,'pizzaman':p.name})
    # Maybe also add in a list of current orders??

def cancel(request):
    # Find way to add order details and include as argument
    return render(request, 'form/cancel.html')