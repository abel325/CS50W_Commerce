from .models import AuctionCategory

def categories_processor(request):
    categories = AuctionCategory.objects.all()            
    return {'categories': categories}