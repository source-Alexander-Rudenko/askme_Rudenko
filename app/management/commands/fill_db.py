import random
import time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import transaction
from app.models import Profile, Question, Answer, Tag, Like

class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio of data to fill')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        
        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_user_ratings = ratio * 200

        self.stdout.write(f'Filling database with ratio {ratio}...')
        
        start_time = time.time()  # Start the timer

        try:
            with transaction.atomic():
                # Bulk create users and profiles
                users = [User(username=f'user_{i}', email=f'user_{i}@example.com') for i in range(num_users)]
                User.objects.bulk_create(users, batch_size=1000)
                self.stdout.write(f'Created {num_users} users.')

                profiles = [Profile(user=user, name=f'User {i}', rating=random.randint(0, 100)) for i, user in enumerate(User.objects.all())]
                Profile.objects.bulk_create(profiles, batch_size=1000)
                self.stdout.write(f'Created {num_users} profiles.')

                # Get all profiles
                profiles = Profile.objects.all()

                # Bulk create tags
                tags = [Tag(name=f'tag_{i}') for i in range(num_tags)]
                Tag.objects.bulk_create(tags, batch_size=1000)
                self.stdout.write(f'Created {num_tags} tags.')

                # Get all tags
                tags = Tag.objects.all()

                # Bulk create questions
                questions = [
                    Question(title=f'Question {i}', text='This is a test question', author=random.choice(profiles), created_at=now())
                    for i in range(num_questions)
                ]
                Question.objects.bulk_create(questions, batch_size=1000)
                self.stdout.write(f'Created {num_questions} questions.')

                # Add tags to questions
                for question in Question.objects.all():
                    question.tags.add(*random.sample(list(tags), k=random.randint(1, 5)))
                self.stdout.write(f'Added tags to questions.')

                # Get all questions
                questions = Question.objects.all()

                # Bulk create answers
                answers = [
                    Answer(content='This is a test answer', question=random.choice(questions), author=random.choice(profiles), created_at=now())
                    for i in range(num_answers)
                ]
                Answer.objects.bulk_create(answers, batch_size=1000)
                self.stdout.write(f'Created {num_answers} answers.')

                # Bulk create likes
                likes = [
                    Like(from_user=random.choice(profiles), to_question=random.choice(questions))
                    for i in range(num_user_ratings)
                ]
                Like.objects.bulk_create(likes, batch_size=1000)
                self.stdout.write(f'Created {num_user_ratings} likes.')

            end_time = time.time()  # End the timer

            elapsed_time = end_time - start_time
            self.stdout.write(self.style.SUCCESS(f'Database filled successfully in {elapsed_time:.2f} seconds!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
