from django.shortcuts import render,redirect
from .models import Category
from django.contrib import messages
# Create your views here.

def show_category(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and not request.POST.get('cat_name')== '':
            category_name = request.POST.get('cat_name')
            user_id = request.POST.get('user_id')
            
            if not category_name:
                messages.error(request, 'Category name cannot be empty.')
            elif Category.objects.filter(category_name=category_name, user_id=user_id).exists():
                messages.error(request, 'You have already created this category.')
            else:
                category = Category(category_name=category_name, user_id=user_id)
                category.save()
                return redirect('add_category')
    
        category_list = Category.objects.filter(user_id=0)
        category_user_add = Category.objects.all().filter(user_id=request.user.id)
        context = {
            'category' : category_list,
            'category_user' : category_user_add
        }

    return render(request,'transactions/category.html',context)