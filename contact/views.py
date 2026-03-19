from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm


def contact(request):
    form = ContactForm()
    success = False

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()

            try:
                send_mail(
                    subject=f"[Portfólio] {msg.subject}",
                    message=(
                        f"Nome: {msg.name}\n"
                        f"E-mail: {msg.email}\n"
                        f"Assunto: {msg.subject}\n\n"
                        f"Mensagem:\n{msg.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            success = True
            form = ContactForm()

        if request.htmx:
            return render(request, "contact/partials/form.html", {
                "form": form,
                "success": success,
            })

    return render(request, "contact/contact.html", {
        "form": form,
        "success": success,
    })