from django.shortcuts import render

# Create your views here.


def dashboard(request):
		context = {
			'user': request.user,
		}

		return render(request, 'accounts/dashboard.html', context)


def login(request):
		context = {

		}

		return render(request, 'accounts/login.html', context)


def wishlist(request):
		context = {

		}

		return render(request, 'accounts/wishlist.html', context)