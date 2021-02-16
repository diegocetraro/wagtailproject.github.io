from django.db import models
from wagtail.snippets.models import register_snippet
# Create your models here.

@register_snippet
class Testimonial (models.Model):

    quote = models.TextField(
        blank = False,
        null = False,
        max_length = 500,
    )

    attribution = models.CharField(
        max_length = 50,
        blank = False,
        null = False,
    )

    def __str__(self):
        return f"{self.quote} by {self.attribution}"

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"