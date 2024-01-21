from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from .models import Course, Lesson, Tag, Category, User
from django import forms
from django.contrib.auth.models import Permission
from django.db.models import Count
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Lesson
        fields = '__all__'

class LessonTagInline(admin.StackedInline):
    model = Lesson.tags.through

class LessonAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("css/main.css",)
        }
    list_display = ('id','subject', 'course', 'created_date', 'active')
    list_filter = ('course',"course__subject", 'created_date', 'updated_date')
    search_fields = ('subject', 'course__subject','created_date')
    readonly_fields = ["avatar"]
    inlines = (LessonTagInline,)
    form = LessonForm
    def avatar(self, lesson):
        return mark_safe("<img src='/static/{img_url}' alt = '{alt}' width='120px' />".format(img_url=lesson.image, alt=lesson.subject))



class LessonInline(admin.StackedInline):
    model = Lesson
    pk_name= 'course'




class CourseAdmin(admin.ModelAdmin):
    inlines = (LessonInline,)



class CoursAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống quản lý các khóa học'

    def get_urls(self):
        return [
            path('course-stats/', self.course_stats)
        ] + super().get_urls()
    def course_stats(self, request):
        course_count = Course.objects.count()
        stats = Course.objects.annotate(lesson_count = Count('lessons')).values("id", "subject", "lesson_count")
        return TemplateResponse(request, 'admin/course-stats.html', {
            'course_count': course_count,
            'stats': stats
        })


admin_site = CoursAppAdminSite('mycourse')

admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(User)
admin.site.register(Permission)

# admin_site.register(Category)
# admin_site.register(Course, CourseAdmin)
# admin_site.register(Lesson, LessonAdmin)