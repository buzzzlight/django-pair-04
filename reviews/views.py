from django.shortcuts import render, redirect
from .forms import CommentForm, ReviewForm
from .models import Review
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
@login_required
def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("reviews:index")
    else:
        review_form = ReviewForm()
    context = {"review_form": review_form}
    return render(request, "reviews/create.html", context=context)


@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                review_form.save()
                return redirect("reviews:detail", review.pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {"review_form": review_form}
        return render(request, "reviews/update.html", context)
    else:
        return redirect("reviews:detail", review.pk)


@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    if request.user == review.user:
        if request.method == "POST":
            review.delete()
            return redirect("reviews:index")
    else:
        return redirect("reviews:detail", review.pk)


def index(request):
    page = request.GET.get("page", "1")
    reviews = Review.objects.order_by("-created_at")
    paginator = Paginator(reviews, 12)
    page_obj = paginator.get_page(page)
    context = {"reviews": page_obj}
    return render(request, "reviews/index.html", context)


def detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = review.comment_set.all()
    context = {
        "review": review,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "reviews/detail.html", context)


# comments
def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect("reviews:detail", review.pk)


def comment_delete(request, review_pk, comment_pk):
    review = Review.objects.get(pk=review_pk)
    comment = review.comment_set.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == "POST":
            comment.delete()
    return redirect("reviews:detail", review.pk)

def search(request):
    search = request.GET.get("search")
    page = request.GET.get("page", "1")
    reviews = Review.objects.filter(title__contains=search).order_by("-created_at")
    paginator = Paginator(reviews, 12)
    page_obj = paginator.get_page(page)
    if  len(search) == 0:
        reviews = []
        text = "검색어를 입력하세요."

    elif len(reviews) == 0:
        text = "검색 결과가 없습니다."
        
    else:
        print(reviews)
        text = ""
        
    context = {
        "reviews" : page_obj,
        "text" : text,
    }
    return render(request, 'reviews/index.html', context)