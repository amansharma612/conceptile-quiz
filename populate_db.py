# populate_db.py
import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz.settings')
django.setup()

from quizapp.models import Topic, Question, Choice

def create_sample_data():
    # Clear existing data
    Choice.objects.all().delete()
    Question.objects.all().delete()
    Topic.objects.all().delete()

    # Sample topics with questions and answers
    topics_data = {
        'Python Programming': [
            {
                'question': 'What is Python?',
                'choices': [
                    ('A high-level programming language', True),
                    ('A type of snake', False),
                    ('A database management system', False),
                    ('A web browser', False),
                ]
            },
            {
                'question': 'Which of these is a valid Python variable name?',
                'choices': [
                    ('my_variable', True),
                    ('2variable', False),
                    ('my-variable', False),
                    ('class', False),
                ]
            },
            {
                'question': 'What is the output of: print(2 ** 3)?',
                'choices': [
                    ('8', True),
                    ('6', False),
                    ('5', False),
                    ('9', False),
                ]
            }
        ],
        'Web Development': [
            {
                'question': 'What does HTML stand for?',
                'choices': [
                    ('HyperText Markup Language', True),
                    ('High Technical Modern Language', False),
                    ('HyperText Modern Links', False),
                    ('High Text Markup Language', False),
                ]
            },
            {
                'question': 'Which tag is used for creating a hyperlink in HTML?',
                'choices': [
                    ('<a>', True),
                    ('<link>', False),
                    ('<href>', False),
                    ('<url>', False),
                ]
            }
        ],
        'Mathematics': [
            {
                'question': 'What is the square root of 144?',
                'choices': [
                    ('12', True),
                    ('14', False),
                    ('10', False),
                    ('16', False),
                ]
            },
            {
                'question': 'What is 15% of 200?',
                'choices': [
                    ('30', True),
                    ('25', False),
                    ('35', False),
                    ('40', False),
                ]
            },
            {
                'question': 'What is the value of π (pi) to 2 decimal places?',
                'choices': [
                    ('3.14', True),
                    ('3.16', False),
                    ('3.12', False),
                    ('3.18', False),
                ]
            }
        ]
    }

    # Create topics and their questions
    for topic_name, questions_data in topics_data.items():
        # Create topic
        topic = Topic.objects.create(
            name=topic_name,
            description=f"Test your knowledge in {topic_name}"
        )
        
        # Create questions for this topic
        for q_data in questions_data:
            question = Question.objects.create(
                topic=topic,
                text=q_data['question']
            )
            
            # Create choices for this question
            for choice_text, is_correct in q_data['choices']:
                Choice.objects.create(
                    question=question,
                    text=choice_text,
                    is_correct=is_correct
                )

    print("Sample data has been populated successfully!")
    print("\nCreated Topics:")
    for topic in Topic.objects.all():
        print(f"\n- {topic.name}")
        print(f"  Questions: {topic.questions.count()}")
        for question in topic.questions.all():
            print(f"    * {question.text}")
            for choice in question.choices.all():
                print(f"      - {choice.text} ({'Correct' if choice.is_correct else 'Incorrect'})")

if __name__ == '__main__':
    print("Starting to populate database...")
    create_sample_data()