from django import forms
from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from course.models import Course, Category, Lesson, Comment, Tag, Like, User
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path


class MyCourseAdmin(admin.AdminSite):
    site_header = "eCourseLine"
    site_title = "My Course Admin Portal"
    index_title = "Welcome to My Course Admin Portal"

    def get_urls(self):
        return [path('course-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        course_stats = Category.objects.annotate(c=Count('course__id')).values("id","name","c")

        return TemplateResponse(request, "admin/stats.html",{
            "course_stats": course_stats
        })


admin_site = MyCourseAdmin(name="iCourse")


class CorseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Course
        fields = "__all__"


class MyCourseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "active"]
    search_fields = ["id", "name"]
    list_filter = ["created_date", "name"]
    readonly_fields = ["my_image"]
    form = CorseForm

    def my_image(self, course):
        if course.image:
            return mark_safe(f"<img src='/static/{course.image.name}' width='200' />")


admin_site.register(Category)
admin_site.register(Lesson)
admin_site.register(Like)
admin_site.register(Comment)
admin_site.register(Tag)
admin_site.register(Course, MyCourseAdmin)
admin_site.register(User)

# Register your models here.
