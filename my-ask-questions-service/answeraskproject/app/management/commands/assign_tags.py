from django.core.management.base import BaseCommand
from app.models import Question, Tag
import random


class Command(BaseCommand):
    help = 'Assigns 3 to 5 random tags to each question'

    def handle(self, *args, **kwargs):
        questions = list(Question.objects.all())
        tags = list(Tag.objects.all())

        for question in questions:
            random_tags = random.sample(tags, k=random.randint(3, 5))
            question.tags.set(random_tags)

        self.stdout.write(self.style.SUCCESS('Successfully assigned tags to questions'))