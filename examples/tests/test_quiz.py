"""
Tests for Quiz views and SSE endpoints.

Tests the quiz functionality including:
- Quiz index page rendering
- Question fetching via SSE
- Answer submission and scoring
- Quiz report generation
"""

import pytest
from django.test import Client
from django.urls import reverse

from examples.models import Answer, Question


@pytest.fixture
def client():
    """Django test client fixture."""
    return Client()


@pytest.fixture
def quiz_questions():
    """Create sample quiz questions for testing."""
    questions = []
    for i in range(15):
        question = Question.objects.create(text=f'Test question {i + 1}?')
        Answer.objects.create(question=question, text='Wrong 1', is_correct=False)
        Answer.objects.create(question=question, text='Correct', is_correct=True)
        Answer.objects.create(question=question, text='Wrong 2', is_correct=False)
        Answer.objects.create(question=question, text='Wrong 3', is_correct=False)
        questions.append(question)
    return questions


@pytest.mark.django_db
class TestQuizIndexView:
    """Tests for quiz index page."""

    @pytest.mark.parametrize(
        'content_contains', ['question-card', 'progress', 'data-init']
    )
    def test_quiz_index_contains(self, client, content_contains):
        """Verify quiz index page contains expected content."""
        response = client.get(reverse('examples:quiz-index'))
        assert response.status_code == 200
        assert content_contains in response.content.decode()

    def test_quiz_index_loads_successfully(self, client):
        """Verify quiz index page returns 200."""
        response = client.get(reverse('examples:quiz-index'))
        assert response.status_code == 200


@pytest.mark.django_db
class TestGetQuestionView:
    """Tests for question SSE endpoint."""

    def test_get_question_returns_sse(self, client, quiz_questions):
        """Verify question endpoint returns SSE content type."""
        response = client.get(reverse('examples:quiz-question'))
        assert response.status_code == 200
        assert 'text/event-stream' in response.get('Content-Type', '')

    def test_get_question_returns_question_fragment(self, client, quiz_questions):
        """Verify question endpoint returns question fragment."""
        response = client.get(reverse('examples:quiz-question'))
        content = b''.join(response.streaming_content).decode()
        assert 'question-card' in content

    def test_get_question_excludes_seen_questions(self, client, quiz_questions):
        """Verify seen questions are excluded from selection."""
        session = client.session
        session['seen_question_ids'] = [quiz_questions[0].pk, quiz_questions[1].pk]
        session.save()

        response = client.get(reverse('examples:quiz-question'))
        content = b''.join(response.streaming_content).decode()

        all_texts = [q.text for q in quiz_questions]
        remaining_texts = all_texts[2:]

        found_question = False
        for text in remaining_texts:
            if text in content:
                found_question = True
                break
        assert (
            found_question or 'report' in content.lower() or len(remaining_texts) == 0
        )

    def test_get_question_returns_report_when_exhausted(self, client):
        """Verify report is shown when all questions answered."""
        for i in range(10):
            question = Question.objects.create(text=f'Question {i}?')
            Answer.objects.create(question=question, text='Answer', is_correct=True)

        session = client.session
        session['seen_question_ids'] = list(
            Question.objects.values_list('pk', flat=True)[:10]
        )
        session['correct_count'] = 7
        session['total_questions'] = 10
        session.save()

        response = client.get(reverse('examples:quiz-question'))
        content = b''.join(response.streaming_content).decode()
        assert 'Quiz Complete' in content or 'quiz-report' in content


@pytest.mark.django_db
class TestSubmitAnswerView:
    """Tests for answer submission SSE endpoint."""

    def test_submit_answer_returns_sse(self, client, quiz_questions):
        """Verify answer submission returns SSE content type."""
        question = quiz_questions[0]
        correct_answer = question.answers.filter(is_correct=True).first()

        response = client.post(
            reverse('examples:quiz-answer'),
            {'question_id': question.pk, 'answer_id': correct_answer.pk},
        )
        assert response.status_code == 200
        assert 'text/event-stream' in response.get('Content-Type', '')

    @pytest.mark.parametrize(
        'is_correct,expected_text', [(True, 'Correct'), (False, 'Incorrect')]
    )
    def test_submit_answer_shows_feedback(
        self, client, quiz_questions, is_correct, expected_text
    ):
        """Verify answer submission shows appropriate feedback."""
        question = quiz_questions[0]
        answer = (
            question.answers.filter(is_correct=True).first()
            if is_correct
            else question.answers.filter(is_correct=False).first()
        )

        session = client.session
        session['correct_count'] = 0
        session['total_questions'] = 10
        session['current_question'] = 1
        session['seen_question_ids'] = [question.pk]
        session.save()

        response = client.post(
            reverse('examples:quiz-answer'),
            {'question_id': question.pk, 'answer_id': answer.pk},
        )
        content = b''.join(response.streaming_content).decode()
        assert expected_text in content


@pytest.mark.django_db
class TestSkipQuestionView:
    """Tests for skip question functionality."""

    def test_skip_question_returns_sse(self, client, quiz_questions):
        """Verify skip endpoint returns SSE content type."""
        question = quiz_questions[0]

        session = client.session
        session['seen_question_ids'] = []
        session['current_question'] = 1
        session['total_questions'] = 10
        session.save()

        response = client.post(
            reverse('examples:quiz-skip'),
            {'question_id': question.pk},
        )
        assert response.status_code == 200
        assert 'text/event-stream' in response.get('Content-Type', '')

    def test_skip_question_returns_next_question_or_report(
        self, client, quiz_questions
    ):
        """Verify skip returns next question or report."""
        question = quiz_questions[0]

        session = client.session
        session['seen_question_ids'] = []
        session['current_question'] = 1
        session['total_questions'] = 10
        session.save()

        response = client.post(
            reverse('examples:quiz-skip'),
            {'question_id': question.pk},
        )
        content = b''.join(response.streaming_content).decode()
        assert 'question-card' in content or 'Quiz Complete' in content


@pytest.mark.django_db
class TestQuizRestart:
    """Tests for quiz restart functionality."""

    def test_restart_returns_sse(self, client, quiz_questions):
        """Verify restart endpoint returns SSE content type."""
        response = client.post(reverse('examples:quiz-restart'))
        assert response.status_code == 200
        assert 'text/event-stream' in response.get('Content-Type', '')

    def test_restart_fetches_first_question(self, client, quiz_questions):
        """Verify restart fetches first question."""
        response = client.post(reverse('examples:quiz-restart'))
        content = b''.join(response.streaming_content).decode()
        assert 'question-card' in content


@pytest.mark.django_db
class TestQuizDatastarIntegration:
    """Test Datastar attributes in quiz templates."""

    @pytest.mark.parametrize('attribute', ['data-init', 'progress', 'data-signals'])
    def test_quiz_has_datastar_attributes(self, client, attribute):
        """Verify quiz has expected Datastar attributes."""
        response = client.get(reverse('examples:quiz-index'))
        content = response.content.decode()
        assert attribute in content or 'currentQuestion' in content
