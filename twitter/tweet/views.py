from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, userRegestrationForm
from django.shortcuts import get_list_or_404,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweet_list = Tweet.objects.all().order_by('-created_at')
    paginator = Paginator(tweet_list, 6)  # Show 6 tweets per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tweet_list.html', {'page_obj': page_obj})


@login_required
def tweet_create(request):
    if request.method== "POST":
        form= TweetForm(request.POST, request.FILES)
        if form.is_valid:
            tweet= form.save(commit=False)
            tweet.user= request.user
            tweet.save()
            return redirect('tweet_list')

    else:
        form = TweetForm()
    return render(request, 'tweet_form.html',{'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet= get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method=="POST":
        form= TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid:
            tweet= form.save(commit=False)
            tweet.user= request.user
            tweet.save()
            return redirect('tweet_list')

    else:
        form= TweetForm(instance=tweet)
    return render(request, 'tweet_form.html',{'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet= get_object_or_404(Tweet, pk=tweet_id,user= request.user)
    if request.method=='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html',{'tweet': tweet})


def register(request):
    if request.method=='POST':
        form= userRegestrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form= userRegestrationForm()

    return render(request, 'registration/register.html',{'form': form})

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def search_tweets(request):
    query = request.GET.get('q', '').strip()
    tweets = []

    if query:
        users = User.objects.filter(username__icontains=query)
        tweets = Tweet.objects.filter(user__in=users).order_by('-created_at')

    # Pagination: 5 tweets per page
    paginator = Paginator(tweets, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search_results.html', {
        'query': query,
        'page_obj': page_obj,
        'tweets': page_obj.object_list,
    })

def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')

    return render(request, 'user_detail.html', {'user': user, 'tweets': tweets})
