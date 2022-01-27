from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Restaurant, News, History
from django.views.generic import DetailView
from .forms import UserRegistrationForm, UserEditForm, AddToHistory
from django.contrib import messages
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class NewsView(DetailView):
    """Dynamic View of page with News"""
    model = News
    template_name = 'web/news_view.html'
    context_object_name = 'news'


def index(request):
    """Index view, renders news about places with pagination """
    news = News.objects.all()
    paginator = Paginator(news, 5)  # 5 posts in each page
    page = request.GET.get('page')  # get page
    try:
        all_news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        all_news = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        all_news = paginator.page(paginator.num_pages)
    return render(request, 'web/index.html', {'page': page,
                                              'news': all_news
                                              })


@login_required
def history(request):
    """renders places, which user have visited with pagination"""
    history_of_places = History.objects.filter(user=request.user)
    paginator = Paginator(history_of_places, 5)  # 5 posts in each page
    page = request.GET.get('page')  # get page
    try:
        places_history = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        places_history = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        places_history = paginator.page(paginator.num_pages)
    return render(request, 'web/history.html', {'page': page,
                                                'history': places_history
                                                })


def places(request, tag_slug=None):
    """renders places with pagination

    -all places if no tags (tag_slugs) were given
    -otherwise renders places, that match particular tags
    """
    places_to_visit = Restaurant.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        places_to_visit = places_to_visit.filter(tags__in=[tag])

    paginator = Paginator(places_to_visit, 5)  # 5 posts in each page
    page = request.GET.get('page')             # get page
    try:
        all_places = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        all_places = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        all_places = paginator.page(paginator.num_pages)
    return render(request, 'web/places.html', {'page': page,
                                               'places': all_places,
                                               'tag': tag})


class PlacesView(DetailView):
    """ renders a particular (dynamic) place"""
    model = Restaurant
    template_name = 'web/places_view.html'

    def get_context_data(self, **kwargs):
        """context def, that returns context of place"""

        context = super(PlacesView, self).get_context_data(**kwargs)    # get context of place
        place = get_object_or_404(Restaurant, id=self.kwargs['pk'])
        added = False
        if place.favourites.filter(id=self.request.user.id).exists():
            added = True                                       # added = True if place already in wishlist

        for element in place.place_location.all():
            context['location_url'] = element.map_location     # getting location_url of a place
        context['menu_images'] = place.menu_images.all()       # give menu  pic of a place
        context['added'] = added
        return context


def about(request):
    """renders about page"""
    return render(request, 'web/about.html')


def register(request):
    """renders registration page"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'web/register_done.html', {'new_user': new_user})
        else:
            return render(request, 'web/register.html', {'user_form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'web/register.html', {'user_form': user_form})


@login_required
def edit(request):
    """renders edit-profile page """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'web/edit.html', {'user_form': user_form})


@login_required
def favourite_add(request, pk):
    """renders adding to wishlist actions"""

    place = get_object_or_404(Restaurant, id=request.POST.get('restaurant_id'))
    if place.favourites.filter(id=request.user.id).exists():
        place.favourites.remove(request.user)
    else:
        place.favourites.add(request.user)
    return HttpResponseRedirect(reverse('places_info', args=[str(pk)]))


@login_required
def wishlist(request):
    """renders wishlist page with pagination"""
    wishlist_elements = request.user.favourites.all()
    paginator = Paginator(wishlist_elements, 10)  # 10 posts in each page
    page = request.GET.get('page')  # get page
    try:
        wishlist_items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        wishlist_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        wishlist_items = paginator.page(paginator.num_pages)
    return render(request, 'web/wishlist.html', {'page': page,
                                                 'wishlist': wishlist_items
                                                 })


@login_required
def add_history(request):
    """renders add_to_history page"""
    error = ''
    if request.method == 'POST':
        given_form = AddToHistory(request.POST)
        if given_form.is_valid():
            element = given_form.save(commit=False)
            element.user = request.user
            element.save()
            return redirect('history')
        else:
            error = 'Проверьте введенные данные'
    form = AddToHistory()
    data = {
        'form': form,
        'error': error,
    }
    return render(request, 'web/add_history.html', data)
