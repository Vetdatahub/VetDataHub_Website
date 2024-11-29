from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from datetime import timedelta
from django.utils.timezone import now
from datasets.models import Dataset


User = get_user_model()


class Discussion(models.Model):
    """
    Represents a discussion thread associated with a specific dataset.
    """

    title = models.CharField(
        max_length=255, help_text="Title of the discussion."
    )
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name="discussions",
        help_text="The dataset this discussion is related to.",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_discussions",
        help_text="The user who started the discussion.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the discussion was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the discussion was last updated.",
    )
    slug = models.SlugField(
        unique=True, blank=True, help_text="Slug for the discussion."
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Represents a comment on a discussion thread.
    """

    discussion = models.ForeignKey(
        Discussion,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The discussion this comment belongs to.",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The user who created the comment.",
    )
    content = models.TextField(help_text="Content of the comment.")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the comment was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the comment was last updated."
    )

    def __str__(self):
        return f"Comment by {self.created_by} on {self.discussion}"

    def is_editable(self):
        """
        Determines if the comment can still be edited (10-minute window).
        """
        return now() <= self.created_at + timedelta(minutes=10)
