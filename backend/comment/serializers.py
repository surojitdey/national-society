from rest_framework import serializers
from comment.models import Comments, Reply, LikeDislike

class CommentSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
      read_only=True,
      slug_field='id'
  )
  full_name = serializers.CharField(source='user.full_name', read_only=True)
  post = serializers.SlugRelatedField(
      read_only=True,
      slug_field='id'
  )
  post_title = serializers.CharField(source='post.title', read_only=True)

  class Meta:
    model = Comments
    fields = (
        'id',
        'user',
        'post',
        'text',
        'added',
        'full_name',
        'post_title'
    )


class DeleteCommentSerializer(serializers.Serializer):
  comment_id = serializers.CharField(max_length=20)


class ReplySerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
      read_only=True,
      slug_field='id'
  )
  full_name = serializers.CharField(source='user.full_name', read_only=True)
  comment = serializers.SlugRelatedField(
      read_only=True,
      slug_field='id'
  )
  post = serializers.CharField(source='comment.post', read_only=True)
  post_title = serializers.CharField(source='comment.post_title', read_only=True)

  class Meta:
    model = Reply
    fields = (
        'id',
        'user',
        'comment',
        'text',
        'added',
        'post',
        'full_name',
        'post_title'
    )


class DeleteReplySerializer(serializers.Serializer):
  reply_id = serializers.CharField(max_length=20)


class LikeDislikeSerializer(serializers.ModelSerializer):
  user = serializers.SlugRelatedField(
      read_only=True,
      slug_field='id'
  )
  full_name = serializers.CharField(source='user.full_name', read_only=True)
  post = serializers.SlugRelatedField(
      read_only=True,
      slug_field='id'
  )
  post_title = serializers.CharField(source='post.title', read_only=True)

  class Meta:
    model = LikeDislike
    fields = (
        'id',
        'user',
        'post',
        'like',
        'dislike',
        'full_name',
        'post_title'
    )
