from django.shortcuts import render, redirect
from .models import Query
from django.contrib import messages

def query(request):
    if request.method == 'POST':
        hadees_number = request.POST.get('hadees_number')
        line_number = request.POST.get('line_number')
        query_text = request.POST.get('query_text')

        new_query = Query(
            hadees_number=hadees_number,
            line_number=line_number,
            query_text=query_text
        )
        new_query.save()
        messages.success(request, "Your query has been submitted successfully.")
        # return redirect('query')

    return render(request, 'query.html')