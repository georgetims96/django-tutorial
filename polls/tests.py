import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Helper method
def create_question(question_text, days):
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
  def test_no_questions(self):
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available.")

  def test_past_question(self):
    question = create_question(question_text="Past question.", days=-30)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(
      response.context['latest_question_list'],
      [question],
    )

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
