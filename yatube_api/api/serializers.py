from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from django.contrib.auth import get_user_model
from posts.models import Comment, Post, Group, Follow


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False, allow_null=True
    )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        fields = ('id', 'text', 'author', 'post', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group 


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = Follow 
        fields = ('user', 'following')
    
    def validate(self, attrs):
        user = self.context['request'].user 
        following = attrs['following']
        if user == following:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя."
            )
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого автора."
            )
        return attrs
