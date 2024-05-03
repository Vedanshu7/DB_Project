from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Book, Comment, Review
from category.models import Category
from checkout.models import order_list
from checkout.models import order
from checkout.models import invoice
from accounts.models  import Account
from checkout.models import invoice
from django.contrib import messages
from django.contrib.auth.decorators import  login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from datetime import datetime
import uuid
from django.db.models import Avg


categories_list = Category.objects.all()


#adding paging


def home(request):

    books = Book.objects.all()[0:20]
    font_page_context = {
        'books': books,
    }
    return render(request, 'index.html',font_page_context)



def contact(request):


    return render(request, 'contact-us.html')

def about(request):

    return render(request, 'about.html')

def single_book(request, single_book_slug):
    if single_book_slug is not None:
        book = get_object_or_404(Book,slug=single_book_slug)
        related_books = Book.objects.filter(genreList__category_id__in=book.genreList.values_list('category_id', flat=True)).exclude(book_id=book.book_id)[:5]
        comments = Comment.objects.all().filter(book=book)
        reviews = Review.objects.all().filter(book=book)
        context = {

            'book': book,
            'related_books': related_books,
            'comments':comments,
            'reviews':reviews
        }

    return render(request, 'book-single-page.html',context)


def search_result(request):
    if 'query' in request.GET:
        q = request.GET['query']
        books = Book.objects.all().filter(title=q)
        print(q)
        print(books)
        context  = {
            'books':books,
        }
        return render(request, 'search_res.html', context)


@login_required(login_url="/login")
def orders(request):
        if request.user.is_authenticated:
            user = Account.objects.get(email=request.user.email)
            order_id = order.objects.all().filter(client=user).order_by('date_created')

            all_orders = Paginator(order.objects.all().filter(client=user).order_by('-date_created'), 10)
            page = request.GET.get('page')

            try:
                orders = all_orders.page(page)
            except PageNotAnInteger:
                orders = all_orders.page(1)
            except EmptyPage:
                orders=  all_orders.page(all_orders.num_pages)

            context={

                'order_id_list' : orders,
            }
            return render(request,"list-orders.html",context)
        else:
            messages.error("Sorry, you need to be logged in to view your orders")
            return redirect("login")

@login_required(login_url="/login")
def view_order(request, order_id):
    if request.user.is_authenticated:
        print(order_id)
        order_items_list = order_list.objects.all().filter(order_id=order_id)
        invoice_details = invoice.objects.all().filter(order_id=order_id)
        full_address = ""
        for invoice_item in invoice_details:
            address_components = [
                invoice_item.address,
                invoice_item.city,
                invoice_item.division,
                invoice_item.zip,
                invoice_item.country
            ]
            address_components = [component for component in address_components if component]
            full_address += ", ".join(address_components)
        context={
            "order_id":order_id,
            "order_items_list":order_items_list,
            "invoice_list": invoice_details,
            "full_address":full_address
        }
        return render(request,"view_order.html",context=context)
    else:
        return redirect('login')


@login_required(login_url="/login")
def view_invoice(request, invoice_id):
    if request.user.is_authenticated:
        invoice_dat = invoice.objects.get(invoice_id=invoice_id)

        context = {

            'invoice':invoice_dat

        }
        return render(request,"view_invoice.html",context=context)
    else:
        return redirect("login")

@login_required(login_url="/login")
def add_review(request, book_slug):
    if request.method == 'POST':
        book = get_object_or_404(Book, slug=book_slug)
        user = request.user
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

        review = Review(review_id  = uuid.uuid4(),book=book, user=user, rating=rating, review_text=review_text, review_date = datetime.now().date())
        review.save()
        
        book_reviews = Review.objects.all().filter(book=book)
        average_rating = 0.0
        if book_reviews.exists():
            ratings = book_reviews.values_list('rating', flat=True)
            average_rating = sum(ratings) / len(ratings)     
        book.average_rating = average_rating
        book.save()
        #messages.success(request, 'Your review has been added.')
        return redirect('single_book', single_book_slug=book_slug)

@login_required(login_url="/login")
def edit_review(request, book_slug, review_id):
    review = get_object_or_404(Review, review_id=review_id)

    if request.method == 'POST':
        rating = request.POST.get('update_rating')
        review_text = request.POST.get('update_review_text')

        review.rating = rating
        review.review_text = review_text
        review.save()

        book = get_object_or_404(Book, slug=book_slug)
        book_reviews = Review.objects.all().filter(book=book)
        average_rating = 0.0
        if book_reviews.exists():
            ratings = book_reviews.values_list('rating', flat=True)
            average_rating = sum(ratings) / len(ratings)      
        book.average_rating = average_rating
        book.save()
        
        #messages.success(request, 'Your review has been updated.')
        return redirect('single_book', single_book_slug=book_slug)

@login_required(login_url="/login")
def delete_review(request, book_slug, review_id):
    review = get_object_or_404(Review, review_id=review_id)
    if request.method == 'POST':
        review.delete()
        
        book = get_object_or_404(Book, slug=book_slug)
        book_reviews = Review.objects.all().filter(book=book)
        average_rating = 0.0
        if book_reviews.exists():
            ratings = book_reviews.values_list('rating', flat=True)
            average_rating = sum(ratings) / len(ratings)    
        book.average_rating = average_rating
        book.save()
        #messages.success(request, 'Your review has been deleted.')
        return redirect('single_book', single_book_slug=book_slug)

@login_required(login_url="/login")
def add_comment(request, book_slug):
    if request.method == 'POST':
        book = get_object_or_404(Book, slug=book_slug)
        user = request.user
        comment_text = request.POST.get('comment_text')

        comment = Comment(comment_id= uuid.uuid4(),book=book, user=user, comment_text=comment_text,comment_date = datetime.now().date())
        comment.save()

        ##messages.success(request, 'Your comment has been added.')
        return redirect('single_book', single_book_slug=book_slug)

@login_required(login_url="/login")
def edit_comment(request, book_slug, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id)

    if request.method == 'POST':
        comment_text = request.POST.get('update_comment_text')

        comment.comment_text = comment_text
        comment.save()

        #messages.success(request, 'Your comment has been updated.')
        return redirect('single_book', single_book_slug=book_slug)

@login_required(login_url="/login")
def delete_comment(request, book_slug, comment_id):
    comment = get_object_or_404(Comment, comment_id=comment_id)

    if request.method == 'POST':
        comment.delete()
        #messages.success(request, 'Your comment has been deleted.')
        return redirect('single_book', single_book_slug=book_slug)




