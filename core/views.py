from django.shortcuts import render
from projects.models import Project


def home(request):
    featured = Project.objects.filter(featured=True).order_by("-created_at")[:3]
    context = {"featured_projects": featured}
    return render(request, "core/home.html", context)
