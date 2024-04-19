from rest_framework import serializers
from course.models import Category, User, Course, Lesson, Comment, Like, Tag
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    # Hiển thị dường dẫn trên cloudinary
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image'] = instance.image.url
        return req

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']


class CourseSerializer(ItemSerializer):

    class Meta:
        model = Course
        fields = ['id','name','image','created_date']


class LessonSerializer(ItemSerializer):

    class Meta:
        model = Lesson
        fields = ['id','subject','image','created_date']


class LessonDetailsSerializer(LessonSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content','tags']


class AuthenticatedLessonDetailsSerializer(LessonDetailsSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, lesson):
        return lesson.like_set.filter(active=True).exists()

    class Meta:
        model = LessonDetailsSerializer.Meta.model
        fields = LessonDetailsSerializer.Meta.fields + ['liked']


class UserSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','password','email','avatar']
        extra_kwargs = {
            'password':{'write_only':True}
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'user']

