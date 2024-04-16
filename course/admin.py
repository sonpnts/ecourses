from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from course.models import Course, Category, Lesson, Comment, Tag, Like
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CorseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Course
        fields = "__all__"


class MyCourseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "active"]
    search_fields = ["id","name"]
    list_filter = ["created_date","name"]
    readonly_fields = ["my_image"]
    form = CorseForm

    def my_image(self,course):
        if course.image:
            return mark_safe(f"<img src='/static/{course.image.name}' width='200' />")


admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Course, MyCourseAdmin)

# Register your models here.
