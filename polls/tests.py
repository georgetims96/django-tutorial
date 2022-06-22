import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Question
# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_too_long_ago(self):
        test_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_question = Question(pub_date=test_time)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_future_question(self):
        test_time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=test_time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_just_in_time(self):
        test_time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        good_question = Question(pub_date=test_time)
        self.assertIs(good_question.was_published_recently(), True)