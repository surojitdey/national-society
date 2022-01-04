from django.urls import path, include
from rest_framework import routers

from comment.views import *

router = routers.DefaultRouter()

router.register('create-comment', SaveCommentViewset)
router.register('delete-comment', DeleteCommentViewset)
router.register('fetch-comments', FetchCommentsViewset)
router.register('create-reply', SaveReplyViewset)
router.register('delete-reply', DeleteReplyViewset)
router.register('like-dislike', LikeDislikeViewset)
router.register('fetch-like-dislike', FetchLikeDislikeViewset)

urlpatterns = [
    path('', include(router.urls))
]
