from store.models import category

def luboh(request):
    babi=category.objects.all()
    return dict(sony=babi)