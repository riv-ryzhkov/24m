from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.views.generic import ListView
from .forms import BookForm
from .models import Book


class IndexTab(ListView):
    paginate_by = 3
    model = Book
    template_name = 'main/index_tab.html'
    context_object_name = 'books'
    extra_context = {'numbers': 'із ' + str(len(Book.objects.all()))}
    allow_empty = False



def index(request):
    # books = Book.objects.all()
    # books = Book.objects.order_by('-id')[:3]
    books = Book.objects.order_by('-id')
    # books = Book.objects.filter(author='Т.Г.Шевченко')
    # books = Book.objects.filter(id__gt=4)
    return render(request, 'main/index.html',
                  {
        'title': 'Головна сторінка',
        'books': books
    })


def about(request):
    context_list = Book.objects.all()
    paginator = Paginator(context_list, 7)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    return render(request, 'main/about.html', {
        'title': 'About site', 'books_page': page_obj
    })




def start(request):
    return render(request, 'main/start.html')

def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = BookForm(initial={'author': 'Невідомий автор'})
    content = {
        'form': form
        }
    return render(request, 'main/create.html', content)

def index_tab(request):
    books = Book.objects.order_by('-id')
    return render(request, 'main/index_tab.html',
                  {
        'title': 'Книги',
        'books': books
    })

def book_view(request, id=1):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        # raise Http404
        book = Book.objects.get(id=1)
    return render(request, 'main/book_view.html',
                  {
        'title': 'Книга',
        'book': book
    })


def book_edit(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = BookForm()
        else:
            book = Book.objects.get(id=id)
            form = BookForm(instance=book)
        return render(request, 'main/book_edit.html', {'form': form})
    else:
        if id == 0:
            form = BookForm(request.POST)
        else:
            book = Book.objects.get(id=id)
            form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('main')

def book_delete(request, id=0):
        try:
            book = Book.objects.get(id=id)
            book.delete()
        except Book.DoesNotExit:
            raise Http404
        return redirect('home')