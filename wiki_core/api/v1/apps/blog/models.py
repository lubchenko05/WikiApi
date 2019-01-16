from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _


CurrentUser = get_user_model()


class Post(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name=_('Title')
    )

    @property
    def editions_count(self):
        return self.post_contents.count()

    @property
    def updated(self):
        return self.post_contents.get(is_published=True).created

    def __str__(self):
        return self.title


class PostContent(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Post',
        related_name='post_contents',
    )
    text = models.TextField(
        verbose_name=_('Text'),
        editable=False,
    )
    author = models.ForeignKey(
        CurrentUser,
        verbose_name='Author',
        on_delete=models.SET_NULL,
        null=True
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_('Is published')
    )

    def save(self, *args, **kwargs):
        super(PostContent, self).save(*args, **kwargs)

        if self.is_published:
            self.post.post_contents.exclude(pk=self.pk).filter(is_published=True).update(is_published=False)

    def __str__(self):
        return '[%s] <%s> %s' % (str(self.created), self.author.email, self.post.title)
