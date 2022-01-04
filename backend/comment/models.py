from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User
from posts.models import Post

class Comments(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE,
                           related_name="user_comment", to_field="id")
  post = models.ForeignKey(Post, on_delete=models.CASCADE,
                           related_name="post_comment", to_field="id")
  text = models.TextField(_("text"), max_length=20000, blank=False)
  added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.post


class Reply(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reply", to_field="id")
  comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name="comment_reply", to_field="id")
  text = models.TextField(_("text"), max_length=20000, blank=False)
  added = models.DateTimeField(auto_now_add=True)


class LikeDislike(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE,
                           related_name="user_response", to_field="id")
  post = models.ForeignKey(Post, on_delete=models.CASCADE,
                           related_name="post_response", to_field="id")
  like = models.BooleanField(_('like'), default=False, blank=False)
  dislike = models.BooleanField(_('dislike'), default=False, blank=False)

  class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['user', 'post'],
            name='unique response'
        )
    ]

