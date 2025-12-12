from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
