from django.shortcuts import render
from core.Utils.Access.decorators import manager_required


@manager_required
def redis_index(request):
    return render(request, 'Admin/Redis/redis_index.html')
