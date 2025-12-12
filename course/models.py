from django.db import models
from django.contrib.auth.models import User


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100)
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=30)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    pub_date = models.DateField()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField()
    mode = models.CharField(max_length=1, choices=[('A', 'Audit'), ('H', 'Honor')])

    def __str__(self):
        return f"{self.learner} enrolled in {self.course}"


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField()

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(id__in=selected_ids, is_correct=True).count()
        if all_answers == selected_correct:
            return True
        else:
            return False

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission for {self.enrollment}"
