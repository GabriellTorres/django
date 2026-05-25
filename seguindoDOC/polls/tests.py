import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choices

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        
        # Set up de varíaveus
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        # Teste
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
    
def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text=question_text, pub_date = time)

class QuestionIndexViewTests(TestCase):

    def text_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are availble')
        self.assertQuerySetEqual(response.context['lasted_question_list'], [])
    
    def test_past_question(self):

        question = create_question(question_text='Past Question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])
    
    def test_future_question(self):

        create_question(question_text='Future Question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):

        question = create_question(question_text='Past Question', days=-30)

        create_question(question_text='Future Question', days=30)

        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])
    
    def test_two_past_question(self):

        # Etapa de set up
        question1 = create_question(question_text='Past Question 1', days=-20)

        question2 = create_question(question_text='Past Question 2', days=-40)
        
        
        # Epata de verificação
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question1, question2])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text='Future Question', days=5)

        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):

        past_question = create_question(question_text='Past Question', days=-20)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

def create_choices(question, choice_text):
    votes = 0
    return Choices.objects.create(question,choice_text, votes)


class QuestionResultsViewTest(TestCase):

    def test_display_results(self):

        # Criando questões
        question = create_question('Qualquer Coisa', days=-10)
        choice1 = create_choices(question=question, choice_text='Resposta1')
        choice2 = create_choices(question=question, choice_text='Resposta2')
        choice3 = create_choices(question=question, choice_text='Resposta3')

        # Deve listar
        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains()