# cafe_core/views.py
from django.shortcuts import render, redirect # Add redirect
from .models import MenuItem, ContactMessage # Add ContactMessage
from django.contrib import messages # For feedback messages


def index_view(request):
    return render(request, 'cafe_core/index.html')

def menu_view(request):
    menu_items = MenuItem.objects.filter(is_available=True)
    context = {
        'menu_items_by_category': {}
    }
    for item in menu_items:
        if item.category not in context['menu_items_by_category']:
            context['menu_items_by_category'][item.category] = []
        context['menu_items_by_category'][item.category].append(item)
    return render(request, 'cafe_core/menu.html', context)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_body = request.POST.get('message') # 'message' is field name in HTML

        # Basic server-side validation
        if name and email and message_body:
            ContactMessage.objects.create(name=name, email=email, message=message_body)
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            # Redirect to the same page (or a thank you page) to prevent re-submission on refresh
            return redirect('cafe_core:contact')
        else:
            messages.error(request, 'Please fill in all fields.')
            # If error, re-render the form with an error message
            # (data is lost here, a Django Form object would handle this better by repopulating)
            return render(request, 'cafe_core/contact.html', {'error': 'Please fill in all fields.'})

    return render(request, 'cafe_core/contact.html')
