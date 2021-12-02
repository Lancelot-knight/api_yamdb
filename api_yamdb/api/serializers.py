from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, User, Review, Comment


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']

    def validate(self, attrs):
        username = attrs.get('username')

        if username == 'me':
            raise serializers.ValidationError('Запрещенное имя для пользователя')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ConfirmationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre
        lookup_field = "slug"


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = "__all__"
        model = Title


class TitleWriteSerializer(TitleReadSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    title = serializers.SlugRelatedField(
        queryset=Title.objects.all(),
        slug_field='name',
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Один автор не может оставить 2 отзыва!'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment
