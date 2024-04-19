from rest_framework import viewsets, generics, status, parsers, permissions
from course.models import Category, User, Course, Lesson, Comment, Like
from course import serializers, paginators, perms
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.CoursePaginator

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)

        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            queryset = queryset.filter(category_id=cate_id)

        return queryset

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lesson(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
        return Response(serializers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)

        q = request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)

        return Response(serializers.LessonSerializer(lessons, many=True).data,
                        status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailsSerializer

    def get_permissions(self):
        if self.action in ['like','add_comment']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return serializers.AuthenticatedLessonDetailsSerializer

        return self.serializer_class

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comment(self, request, pk):
        comments= self.get_object().comment_set.select_reload('user').order_by('-id')


        paginator = paginators.CommentPaginator()
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            return paginator.get_paginated_response(serializers.CommentSerializer(page, many=True).data)


        return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)



    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self,request,pk):
        c = self.get_object().comment_set.create(content=request.data['content'], user=request.user)

        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)
    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        li,created = Like.objects.get_or_create(lesson=self.get_object(), user=request.user)

        if not created:
            li.active = not li.active
            li.save()

        return Response(serializers.AuthenticatedLessonDetailsSerializer(self.get_object()).data)

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes =  [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action in ['get_current_user']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method == 'PATCH':
            for k,v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(request.user).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.CommentOwner]


