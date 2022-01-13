from .models import Category

def menu_links(request):
  links = Category.objects.all()
  # dict(kwargs) -> create a dictionary with key=value
  return dict(links=links)