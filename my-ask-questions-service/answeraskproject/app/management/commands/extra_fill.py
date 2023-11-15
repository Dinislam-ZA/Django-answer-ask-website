# myapp/management/commands/fill_db.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, Like, Profile, LikeAnswer
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Fills the database with test data'

    def handle(self, *args, **options):

        ratio = 5000

        users = list(User.objects.all())

        answers = list(Answer.objects.all())



        likesans = []
        for _ in range(ratio * 200):
            likesans.append(LikeAnswer(
                user=random.choice(users),
                answer=random.choice(answers),
                is_positive=random.choice([True, False])  # Рандомно выбираем тип оценки
            ))
        LikeAnswer.objects.bulk_create(likesans)

        self.stdout.write(self.style.SUCCESS('Successfully filled the database'))