from django.shortcuts import render
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import permission_classes

from service_auth.permissions import IsAdminUser, IsUser, IsUserReadOnly
from users.models import User
from posts.models import Post
from comment.models import Comments, Reply, LikeDislike
from comment.serializers import CommentSerializer, DeleteCommentSerializer, ReplySerializer, LikeDislikeSerializer, DeleteReplySerializer
from helpers.pagination import CommentPagination


class FetchCommentsViewset(viewsets.ModelViewSet):
  queryset = Comments.objects.all()
  serializer_class = CommentSerializer
  permission_classes = [AllowAny]
  pagination_class = CommentPagination

  def list(self, request):
    post = self.request.query_params.get('post')
    if post:
      comments = Comments.objects.filter(post=post).order_by('added')
      comment_count = Comments.objects.filter(post=post).order_by('added').count()
      page = self.paginate_queryset(comments)
      serializer_context = {'request': request}
      serializer = self.serializer_class(page, context=serializer_context, many=True)

      # for comment in serializer.data:
      for (index, comment) in enumerate(comments):
        serializer.data[index]['can_delete'] = self.request.user.id in [
            comment.user.id, comment.post.user.id]
        # replies = Reply.objects.filter(comment=comment['id'])
        # comment_count += Reply.objects.filter(comment=comment['id']).count()
        replies = Reply.objects.filter(comment=comment.id)
        comment_count += Reply.objects.filter(comment=comment.id).count()
        if len(replies) > 0:
          reply_serializer = ReplySerializer(replies, many=True)
          for (reply_index, reply) in enumerate(replies):
            reply_serializer.data[reply_index]['can_delete'] = self.request.user.id in [
                reply.user.id, reply.comment.post.user.id]
          serializer.data[index]['replies'] = reply_serializer.data
      
      return self.get_paginated_response(serializer.data)
    else:
      return Response({
        'status': False,
        'details': 'Post id is missing'
      }, status=status.HTTP_400_BAD_REQUEST)


class FetchLikeDislikeViewset(viewsets.ModelViewSet):
  queryset = LikeDislike.objects.all()
  serializer_class = LikeDislikeSerializer
  permission_classes = [AllowAny]

  def list(self, request):
    post = self.request.query_params.get('post')
    like = LikeDislike.objects.filter(post=post, like=True).count()
    dislike = LikeDislike.objects.filter(post=post, dislike=True).count()
    # serializer = self.serializer_class(like, many=True)
    
    return Response({
      'status': True,
      'like': like,
      'dislike': dislike,
      'detail': 'Comments are fetched.'
    }, status=status.HTTP_200_OK)


class SaveCommentViewset(viewsets.ViewSet):
  queryset = Comments.objects.all()
  serializer_class = CommentSerializer
  permission_classes = [IsUser | IsAdminUser]

  def create(self, request):
    if self.request.user:
      if 'post' in request.data:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        try:
          post = Post.objects.get(id=self.request.data.get('post'))
          serializer.save(user=self.request.user, post=post, text=self.request.data.get('text'))
        except:
          return Response({
            'status': False,
            'detail': serializer.errors
          }, status=status.HTTP_417_EXPECTATION_FAILED)
        return Response({
            'status': True,
            'detail': 'Comment created.'
        }, status=status.HTTP_201_CREATED)
      else:
        return Response({
            'status': False,
            'detail': 'Post not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response({
          'status': False,
          'detail': 'User not found'
      }, status=status.HTTP_404_NOT_FOUND)


class DeleteCommentViewset(viewsets.ViewSet):
  queryset = Comments.objects.all()
  serializer_class = DeleteCommentSerializer
  permission_classes = [IsUser | IsAdminUser]

  def create(self, request):
    if self.request.user:
      if self.request.data.get('comment_id'):
        try:
          comment = Comments.objects.get(id=self.request.data.get('comment_id'))
          if (comment.user == self.request.user) or (self.request.user == comment.post.user):
            comment.delete()
          else:
            return Response({
              'status': False,
              'details': "You are not authorize to delete another person's comments"
            }, status=status.HTTP_403_FORBIDDEN)
        except:
          return Response({
            'status': False,
            'detail': 'Something wrong.'
          }, status=status.HTTP_417_EXPECTATION_FAILED)
        return Response({
          'status': True,
          'detail': 'Comment deleted.'
        }, status=status.HTTP_204_NO_CONTENT)
      else:
        return Response({
          'status': False,
          'detail': 'Comment not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    else:
      return Response({
          'status': False,
          'detail': 'User not found.'
      }, status=status.HTTP_404_NOT_FOUND)


class DeleteReplyViewset(viewsets.ViewSet):
  queryset = Reply.objects.all()
  serializer_class = DeleteReplySerializer
  permission_classes = [IsUser | IsAdminUser]

  def create(self, request):
    if self.request.user:
      if 'reply_id' in self.request.data:
        try:
          reply = Reply.objects.get(id=self.request.data.get('reply_id'))
          # print('***********')
          # print(comment.user)
          # print(self.request.user)
          # print(self.request.user == comment.user)
          # print(comment.post.user)
          # print('***********')
          if (reply.user == self.request.user) or (self.request.user == reply.comment.post.user):
            reply.delete()
          else:
            return Response({
              'status': False,
              'details': "You are not authorize to delete another person's comments"
            }, status=status.HTTP_403_FORBIDDEN)
        except:
          return Response({
            'status': False,
            'detail': 'Something wrong.'
          }, status=status.HTTP_417_EXPECTATION_FAILED)
        return Response({
          'status': True,
          'detail': 'Reply deleted.'
        }, status=status.HTTP_204_NO_CONTENT)
      else:
        return Response({
          'status': False,
          'detail': 'Reply not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    else:
      return Response({
          'status': False,
          'detail': 'User not found.'
      }, status=status.HTTP_404_NOT_FOUND)


class SaveReplyViewset(viewsets.ViewSet):
  queryset = Reply.objects.all()
  serializer_class = ReplySerializer
  permission_classes = [IsUser | IsAdminUser]

  def create(self, request):
    if self.request.user:
      if 'comment' in request.data:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        try:
          comment = Comments.objects.get(id=self.request.data.get('comment'))
          serializer.save(user=self.request.user, comment=comment,
                          text=self.request.data.get('text'))
        except:
          return Response({
              'status': False,
              'detail': serializer.errors
          }, status=status.HTTP_417_EXPECTATION_FAILED)
        return Response({
            'status': True,
            'data': serializer.data,
            'detail': 'Reply created.'
        }, status=status.HTTP_201_CREATED)
      else:
        return Response({
            'status': False,
            'detail': 'Comment not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response({
          'status': False,
          'detail': 'User not found'
      }, status=status.HTTP_404_NOT_FOUND)


class LikeDislikeViewset(viewsets.ViewSet):
  queryset = LikeDislike.objects.all()
  serializer_class = LikeDislikeSerializer
  permission_classes = [IsUser | IsAdminUser]

  def create(self, request):
    if self.request.user:
      if 'post' in request.data:
        post = Post.objects.get(id=self.request.data.get('post'))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        try:
          serializer.save(user=self.request.user, post=post,
                          like=self.request.data.get('like'), dislike=self.request.data.get('dislike'))
        except IntegrityError:
          try:
            like = LikeDislike.objects.get(user=self.request.user, post=post)
            like.like = self.request.data.get('like')
            like.dislike = self.request.data.get('dislike')
            like.save()
          except (ObjectDoesNotExist, MultipleObjectsReturned):
            return Response({
                'status': False,
                'detail': 'Response does not exist or multiple objects returned.'
            }, status=status.HTTP_417_EXPECTATION_FAILED)
          return Response({
              'status': True,
              'detail': 'Response updated'
          }, status=status.HTTP_200_OK)
        return Response({
            'status': True,
            'detail': 'Response created.'
        }, status=status.HTTP_201_CREATED)
      else:
        return Response({
            'status': False,
            'detail': 'Comment not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response({
          'status': False,
          'detail': 'User not found'
      }, status=status.HTTP_404_NOT_FOUND)
