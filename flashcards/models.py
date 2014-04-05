from django.db import models
from django.db.models.query import QuerySet
from django.conf import settings
from django.utils import timezone
import datetime
import random
import json

class FlashCardManager(models.Manager):
    def random(self):
        count = self.count()
        success = False
        while not success:
            random_index = random.randint(1, count)
            try:
                card = self.get(id=random_index)
                return card
            except Exception, e:
                print e

class FlashCard(models.Model):
    word = models.CharField(max_length=32,)
    definition=models.TextField()

    objects = FlashCardManager()

    def __unicode__(self):
        return self.word

    def as_json(self):
        d =  {'word': self.word,
              'definition': self.definition
             }
        return json.dumps(d)

    class Meta:
        permissions = (('can_play', 'Can use FlashCard app'),
                       ('admin', 'Administrate FlashCard users'),
                        )

class UserFlashCard(models.Model):
    '''
    Business Logic:
    - Each user-word starts out in box 0.
    - If a user gets a word right, it increases to the next box, up to box 11.
    - If a user gets a word wrong, it goes back to box 1.

    - Box 1-11 are associated with the following timespans:  5 seconds, 25 seconds, 2 minutes, 10 minutes, 1 hour, 5 hours, 1 day, 5 days, 25 days, 4 months, and never.
    - The timespans reflect the amount of time to wait before the next review

    - Forgetting words:
    -- If a user has gotten any single word wrong 10 times ever (even if they got the word right in between; this is a lifetime count), the word gets put into a "hard to remember" box and is never shown again.
    '''
    flashcard = models.ForeignKey(FlashCard)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    box = models.IntegerField(default=0)
    last_shown = models.DateTimeField(auto_now=True)
    got_wrong = models.IntegerField(default=0)

    def __unicode__(self):
        return u"User %s: word '%s' in box %s" % (self.user, self.flashcard.word, self.box)

    def as_json(self):
        d =  {'word': self.flashcard.word,
              'definition': self.flashcard.definition,
              'box': self.box,
              'last_shown': str(self.last_shown),
              'got_wrong': self.got_wrong,
             }
        return json.dumps(d)

    def needs_review(self):
        intervals = {1: datetime.timedelta(seconds=5),
                     2: datetime.timedelta(seconds=25),
                     3: datetime.timedelta(minutes=2),
                     4: datetime.timedelta(minutes=10),
                     5: datetime.timedelta(hours=1),
                     6: datetime.timedelta(hours=5),
                     7: datetime.timedelta(days=1),
                     8: datetime.timedelta(days=5),
                     9: datetime.timedelta(days=25),
                     10: datetime.timedelta(days=125),
                     }
        if self.got_wrong >= 10:
            return False
        elif self.box == 0:
            return True
        elif self.box >= 11:
            return False
        else:
            return timezone.now() - self.last_shown > intervals[self.box]

    def correct(self):
        self.box += 1

    def incorrect(self):
        self.got_wrong += 1
        self.box = 1

