from django.shortcuts import render
from .models import Category


def category_list(request):
    cats = Category.objects.all()
    cats_list = list(cats)

    result = []
    for cat in cats_list:
        count = cat.get_event_count()
        result.append({
            'category': cat,
            'event_count': count,
        })

    return render(request, 'categories/list.html', {'categories_with_counts': result})
