from rest_framework.serializers import ModelSerializer
from .models import Course, Tag, Lesson, User



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [ "id", "username", "password", "email", "first_name", "last_name", "avatar"]

class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "subject", "image", "category", "created_date"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", "name"]


class LessonSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ["id", "subject", "content" ,"course","image","created_date", "tags"]