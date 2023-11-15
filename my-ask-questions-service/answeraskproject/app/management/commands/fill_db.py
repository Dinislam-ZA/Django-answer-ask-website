# myapp/management/commands/fill_db.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, Like, Profile
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Fills the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The ratio to fill the database')

    def handle(self, *args, **options):
        ratio = options['ratio']
        fake = Faker()

        users = []
        for u in range(ratio):
            users.append(User(
                username=fake.user_name() + u.__str__(),
                email=fake.email() + u.__str__(),
                password=fake.password()
            ))
        User.objects.bulk_create(users)

        tags = []
        for t in range(ratio):
            tags.append(Tag(name=fake.word() + t.__str__()))
        Tag.objects.bulk_create(tags)

        users = list(User.objects.all())

        profiles = [Profile(user=user) for user in users]
        Profile.objects.bulk_create(profiles)

        tags = list(Tag.objects.all())

        questions = []
        for q in range(ratio * 10):
            questions.append(Question(
                title=fake.sentence() + q.__str__(),
                content=fake.text(),
                user=random.choice(users)
            ))
        Question.objects.bulk_create(questions)

        questions = list(Question.objects.all())

        answers = []
        for _ in range(ratio * 100):
            answers.append(Answer(
                question=random.choice(questions),
                content=fake.text(),
                user=random.choice(users)
            ))
        Answer.objects.bulk_create(answers)

        likes = []
        for _ in range(ratio * 200):
            likes.append(Like(
                user=random.choice(users),
                question=random.choice(questions),
                is_positive=random.choice([True, False])  # Рандомно выбираем тип оценки
            ))
        Like.objects.bulk_create(likes)

        self.stdout.write(self.style.SUCCESS('Successfully filled the database'))

