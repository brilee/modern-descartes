from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from .models import UserFlashCard, FlashCard
from django.core.exceptions import ObjectDoesNotExist
import json


def home(request):
    if not request.user.has_perm('flashcards.can_play'):
        return render(request, 'flashcard_forbidden.html')
    return render(request, 'flashcard_home.html')

def admin_index(request):
    if not request.user.has_perm('flashcards.admin'):
        return render(request, 'flashcard_forbidden.html')
    flashcard_users = Group.objects.get(name="flashcard_users").user_set.all()
    return render(request, 'flashcard_admin_index.html', locals())

def admin_profile(request, username):
    if not request.user.has_perm('flashcards.admin'):
        return render(request, 'flashcard_forbidden.html')
    user = get_object_or_404(User, username=username)
    flashcards = UserFlashCard.objects.filter(user=user)
    to_review = [c for c in flashcards if c.needs_review()]
    return render(request, 'flashcard_admin_profile.html', locals())

def getcard(request):
    # this view should only ever be GETed to.
    if request.method != "GET":
        return HttpResponseBadRequest("Invalid HTTP action")

    username = request.GET.get('username', None)
    if username is None:
        return HttpResponseBadRequest("Invalid API request")

    user = get_object_or_404(User, username=username)
    flashcards = UserFlashCard.objects.filter(user=user)
    review_cards = [c for c in flashcards if c.needs_review()]
    if not review_cards:
        # We're all done reviewing cards we've seen before!
        # Pick a random card that the user hasn't seen before.
        # If a UserFlashCard object exists, then the user has seen that flashcard already.
        # If we're having trouble finding a random card, just return one randomly.
        count = 0
        card = FlashCard.objects.random()
        while card in flashcards and count < 5:
            count += 1
            card = FlashCard.objects.random()
    else:
        # If there are cards to be reviewed first, return the one with
        # the highest box number.
        card = sorted(review_cards, key=lambda x: x.box, reverse=True)[0]
    return HttpResponse(card.as_json())

@csrf_exempt
def submit(request):
    # this view should only ever be POSTed to.
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid HTTP action")

    # Currently, no validation to make sure that the same user is the one
    # submitting the correct / incorrect POST requests.
    username = request.POST.get('username', None)
    word = request.POST.get('word', None)
    correct = request.POST.get('correct', None)
    if correct is None or username is None or word is None:
        return HttpResponseBadRequest("Invalid API request: submitted %s" % request.POST)

    user = get_object_or_404(User, username=username)
    flashcard = get_object_or_404(FlashCard, word=word)

    try:
        # See if person has done this word before.
        UFC = UserFlashCard.objects.get(user=user, flashcard=flashcard)
    except ObjectDoesNotExist:
        # Using this word for the first time. Create a new entry.
        UFC = UserFlashCard(user=user, flashcard=flashcard)

    if correct == '1':
        UFC.correct()
    elif correct == '0':
        UFC.incorrect()
    else:
        return HttpResponseBadRequest("Invalid correct parameter, should be 0 or 1")
    UFC.save()

    return HttpResponse("Success")
