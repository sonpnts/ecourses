from django.contrib import admin
from django.utils.html import mark_safe
from course.models import Course, Category


class MyCourseAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_date", "updated_date", "active"]
    search_fields = ["id","name"]
    list_filter = ["created_date","name"]
    readonly_fields = ["my_image"]

    def my_image(self,course):
        if course.image:
            return mark_safe(f"<img src='/static/{course.image.name}' width='200' />")

admin.site.register(Category)
admin.site.register(Course, MyCourseAdmin)

# Register your models here.
