from django.shortcuts import render, redirect
from .models import Message
 
def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")

    # Get all the messages in the table
    messages = Message.objects.values('message', 'username')

    # Pass the messages to the template
    return render(request, "home.html", {'initial_messages': messages})
