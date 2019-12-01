import copy
from typing import Dict, Type

from django.contrib.auth.models import Group, User
from rest_framework import fields, serializers, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from testapp.models import Blog, Comment, Post, PostPhoto


# def make_response_wrapper(request_serializer: Type[serializers.Serializer],
#                           response_serializer: Type[serializers.Serializer]):

#     class ResponseWrapperSerializer(serializers.Serializer):
#         success = fields.BooleanField(read_only=True)
#         result: serializers.Serializer
#         errors: serializers.Serializer


def process_request(request_serializer: Type[serializers.Serializer],
                    response_serializer: Type[serializers.Serializer],
                    data: Dict):
    """
    Реализует базовый флоу 
        для вьюшек создания/редактирования объекта requst_serializer должен наследоваться от ModelSerializer
        для остальных - у входного сериализатора должен быть переопределен метод create()
    """
    input_model = request_serializer(data=data)
    if input_model.is_valid():
        instance = input_model.save()
        output = response_serializer(instance)
        return Response(output.data)
    return Response(input_model.errors)


class CreateBlogRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        # поля из модели в который автоматически подставятся поля из json
        fields = ['title', 'blog_type']

    # кастомное поле которого нет в модели
    blog_type = serializers.CharField(
        min_length=3, max_length=10, allow_blank=False, write_only=True)

    def validate_title(self, value: str):  # кастомная сериализация ОДНОГО поля
        print('validate_title', value)
        if value != value.upper():
            raise serializers.ValidationError({
                'attracted_title': 'ЗАГОЛОВОК ДОЛЖЕН ПРИВЛЕКАТЬ ВНИМАНИЕ!'
            })
        return value

    def get_blog_title(self):
        # генерирует заголовок для блога типа "[Cars] AcademeG"
        blog_type = self.validated_data['blog_type']
        title = self.validated_data['title']
        return f'[{blog_type}] {title}'

    def create(self, validated_data: Dict):
        print('create', validated_data)
        data = copy.deepcopy(validated_data)
        # из-за кастомного поля необходимо выпилить его из validated_date
        data.pop('blog_type')
        obj = Blog.objects.create(**data)  # и переопределить создание объекта
        obj.title = self.get_blog_title()  # здесь делаем какое-то кастомное действие
        obj.save()
        return obj


class CreateBlogResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'some_shit']
    id = fields.ReadOnlyField()
    some_shit = serializers.SerializerMethodField('get_some_shit')

    def get_some_shit(self, obj):
        return f'some shit {obj.pk}'


@api_view(['POST'])
def create_blog(request) -> Response:
    return process_request(CreateBlogRequestSerializer, CreateBlogResponseSerializer, request.data)

############################################################################################################################################################################################################
############################################################################################################################################################################################################
############################################################################################################################################################################################################


class PostPhotoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPhoto
        fields = ['image']

    # пример простого переименования поля (во входных данных: image, в модели: photo)
    image = fields.ImageField(source='photo')


class PostPhotoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPhoto
        fields = ['id']
    id = fields.ReadOnlyField()


@api_view(['POST'])
def upload_post_photo(request) -> Response:
    return process_request(PostPhotoRequestSerializer, PostPhotoResponseSerializer, request.data)


############################################################################################################################################################################################################
############################################################################################################################################################################################################
############################################################################################################################################################################################################

class CreatePostRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'photos', 'blog']

    # В конкретном этом случае велосипед в виде ListField + validate()
    # легко заменяется на PrimaryKeyRelatedField
    photos = serializers.PrimaryKeyRelatedField(
        queryset=PostPhoto.objects.all(),
        many=True)

    # photos = serializers.ListField(write_only=True)
    #
    # def validate_photos(self, value):
    #     # преобразование поля photos в процессе валидации позволяет при create()
    #     # автоматически подставлять объекты ФОТО в пост.
    #     # подобное может пригодиться в велосипедостроительстве
    #     print(value)
    #     def id_to_photo(photo_id: str) -> PostPhoto:
    #         try:
    #             return PostPhoto.objects.get(id=photo_id)
    #         except PostPhoto.DoesNotExist:
    #             raise serializers.ValidationError(
    #                 f'Фотография с идентификатором {photo_id} не найдена')
    #         except:
    #             raise serializers.ValidationError(
    #                 f'При обоработке фотографии с идентификатором {photo_id} что-то пошло не так')
    #     return list(map(id_to_photo, value))


@api_view(['POST'])
def create_post(request) -> Response:
    return process_request(CreatePostRequestSerializer, CreatePostRequestSerializer, request.data)
