from django.shortcuts import render
from core.Utils.Access.decorators import manager_required


@manager_required
def home_index(request):
    return render(request, 'Admin/home_index.html')
