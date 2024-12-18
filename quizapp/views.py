from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from .models import Topic, Quiz, Question, QuizQuestion
import random


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes to fields
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500'
        })


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('topic_selection')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'authentication/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            
            # Redirect to the page user was trying to access, or default to topic selection
            next_page = request.GET.get('next', 'topic_selection')
            return redirect(next_page)
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'authentication/login.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('login')


@login_required
def topic_selection(request):
    topics = Topic.objects.all()
    return render(request, 'quizapp/select_topic.html', {'topics': topics})

@login_required
def create_quiz(request):
    if request.method == 'POST':
        topic_id = request.POST.get('topic')
        topic = Topic.objects.get(id=topic_id)
        
        # Create a new quiz
        quiz = Quiz.objects.create(
            user=request.user,
            topic=topic
        )
        
        # Get all questions for the topic
        questions = list(Question.objects.filter(topic=topic))
        # Randomly select 5 questions (or fewer if there aren't 5)
        selected_questions = random.sample(questions, min(5, len(questions)))
        
        # Create QuizQuestion entries
        for question in selected_questions:
            QuizQuestion.objects.create(
                quiz=quiz,
                question=question
            )
        
        return redirect('take_quiz', quiz_id=quiz.id)
    
    return redirect('topic_selection')

@login_required
def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    quiz_questions = quiz.quiz_questions.all()
    
    if request.method == 'POST':
        # Process quiz submission
        for quiz_question in quiz_questions:
            selected_choice_id = request.POST.get(f'question_{quiz_question.id}')
            if selected_choice_id:
                quiz_question.selected_choice_id = selected_choice_id
                quiz_question.is_correct = quiz_question.selected_choice.is_correct
                quiz_question.save()
        
        quiz.completed_at = timezone.now()
        quiz.save()
        
        return redirect('quiz_results', quiz_id=quiz.id)
    
    context = {
        'quiz': quiz,
        'quiz_questions': quiz_questions
    }
    return render(request, 'quizapp/take_quiz.html', context)

@login_required
def quiz_results(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    quiz_questions = quiz.quiz_questions.all()
    correct_answers = quiz_questions.filter(is_correct=True).count()
    
    context = {
        'quiz': quiz,
        'quiz_questions': quiz_questions,
        'correct_answers': correct_answers,
        'total_questions': quiz_questions.count()
    }
    return render(request, 'quizapp/quiz_results.html', context)