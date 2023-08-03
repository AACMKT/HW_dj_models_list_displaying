from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    content = Book.objects.all().order_by('id')
    context = {'books': content}
    return render(request, template, context)


def books_by_date(request, pub_date):
    template = 'books/filtered.html'
    content = Book.objects.filter(pub_date=pub_date)
    try:
        dates_before = Book.objects.filter(pub_date__lt=pub_date).order_by('pub_date').reverse()[:1]
        prev_page_url = f'{reverse("books")}{dates_before.get().pub_date}'
        pr_page = str(dates_before.get().pub_date)
    except Exception:
        prev_page_url = None
        pr_page = ""
    try:
        dates_after = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date')[:1]
        next_page_url = f'{reverse("books")}{dates_after.get().pub_date}'
        next_page = str(dates_after.get().pub_date)
    except Exception:
        next_page_url = None
        next_page = ""
    paginator = Paginator(content, 10)
    info = paginator.get_page(content)
    return render(request, template, context={
        'books_filtered': info,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
        'prev_date': pr_page,
        'next_date': next_page,
    })
