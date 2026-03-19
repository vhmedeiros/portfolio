from django.shortcuts import render
from .forms import ContactForm


def contact(request):
    form = ContactForm()
    success = False

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()  # limpa o form após envio

        # HTMX: retorna apenas o fragmento do formulário
        if request.htmx:
            return render(request, "contact/partials/form.html", {
                "form": form,
                "success": success,
            })

    return render(request, "contact/contact.html", {
        "form": form,
        "success": success,
    })
