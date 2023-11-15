from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Q


class AnswerManager(models.Manager):
    def get_with_likes(self):
        return self.annotate(
            positive_likes=Count('likeanswer', distinct=True, filter=Q(likeanswer__is_positive=True)),
            negative_likes=Count('likeanswer', distinct=True, filter=Q(likeanswer__is_positive=False))
        )

    def get_answer_by_question(self, question_pk):
        return self.get_with_likes().filter(question__pk=question_pk)


class QuestionManager(models.Manager):
    def get_best_questions(self):
        return self.get_with_likes().annotate(
            rating=Count('like', distinct=True, filter=Q(like__is_positive=True)) -
                   Count('like', distinct=True, filter=Q(like__is_positive=False))
        ).order_by('-rating')

    def get_new_questions(self):
        return self.get_with_likes().order_by('-created_at')

    def get_questions_by_tag(self, tag_name):
        return self.get_with_likes().filter(tags__name=tag_name)

    def get_question_with_likes(self, pk):
        return self.get_with_likes().get(pk=pk)

    def get_with_likes(self):
        return self.annotate(
            positive_likes=Count('like', distinct=True, filter=Q(like__is_positive=True)),
            negative_likes=Count('like', distinct=True, filter=Q(like__is_positive=False)),
            answers_num=Count('answer', distinct=True)
        )


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f"Answer to {self.question.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_positive = models.BooleanField(default=True)

    def __str__(self):
        vote_type = "Positive" if self.is_positive else "Negative"
        return f"{self.user.username} {vote_type} like {self.question.title}"


class LikeAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_positive = models.BooleanField(default=True)

    def __str__(self):
        vote_type = "Positive" if self.is_positive else "Negative"
        return f"{self.user.username} {vote_type} like {self.answer}"
