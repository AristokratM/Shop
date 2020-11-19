from django.shortcuts import render

# Create your views here.


def test_view(requset):
    return render(requset, 'base.html', {})