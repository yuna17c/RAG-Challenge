from django.shortcuts import render
from .forms import MyForm

def my_form_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Do something with the data (e.g., save to a database)

            # For demonstration purposes, you can just display the data in the template
            return render(request, 'myapp/thank_you.html', {'name': name, 'email': email, 'message': message})
    else:
        form = MyForm()

    return render(request, 'my_form_view.html', {'form': form})