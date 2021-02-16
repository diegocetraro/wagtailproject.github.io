from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.models import ParentalKey
from wagtail.core.fields import RichTextField
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.utils.translation import gettext_lazy as _ #***** For FORM FIELD CHOICES of AbstractFormField Class*****#s
# Create your models here.

FORM_FIELD_CHOICES = [
    ('singleline', _('Single line text')),
    ('multiline', _('Multi-line text')),
    ('email', _('Email')),
    ('number', _('Number')),
    ('url', _('URL')),
    ('checkbox', _('Checkbox')),
    ('checkboxes', _('Checkboxes')),
]

#*************************USE IN CASE YOU WANT ALL INPUT CHOICES IN WAGTAIL********************
#FORM_FIELD_CHOICES = (
#    ('singleline', _('Single line text')),
#    ('multiline', _('Multi-line text')),
#    ('email', _('Email')),
#    ('number', _('Number')),
#    ('url', _('URL')),
#    ('checkbox', _('Checkbox')),
#    ('checkboxes', _('Checkboxes')),
#    ('dropdown', _('Drop down')),
#    ('multiselect', _('Multiple select')),
#    ('radio', _('Radio buttons')),
#    ('date', _('Date')),
#    ('datetime', _('Date/time')),
#    ('hidden', _('Hidden field')),
#)

class CustomAbstractFormField(AbstractFormField):
   
    field_type = models.CharField(
        verbose_name = "Field Type",
        max_length = 16,
        choices = FORM_FIELD_CHOICES,
    )

    class Meta:
        abstract = True,
        ordering = ["sort_order"]


class FormField(CustomAbstractFormField):

    form = ParentalKey("ContactPage", on_delete=models.CASCADE, related_name = "form_fields")

class ContactPage(AbstractEmailForm):

    template = "contacts/contact_page.html"
    landing = "contacts/contact_page_landing.html"
    subpage_type = []
    max_count = 1

    intro = RichTextField(
        blank = True,
        features = ["bold", "italic", "link","ol","ul"],
        
    )
    thank_you_text = RichTextField(
       blank = True, 
       features = ["bold", "italic", "link","ol","ul"],
    )
    map_image = models.ForeignKey(
        'wagtailimages.Image',
        null = True,
        blank = False,
        related_name = "+",
        help_text = "Image will be cropped 570px by 370px",
        on_delete = models.SET_NULL
    )
    map_url = models.URLField(
        max_length = 50,
        help_text = "Enter an URL",
        blank = True
    )
    home_page = models.ForeignKey(
        'wagtailcore.Page',
        blank = False,
        null = True,
        related_name="+",
        on_delete = models.SET_NULL
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        FieldPanel("thank_you_text"),
        ImageChooserPanel("map_image"),
        InlinePanel("form_fields", label="Form Field"),
        FieldPanel("map_url"),
        PageChooserPanel("home_page"),
        FieldPanel("from_address"),
        FieldPanel("to_address"),
        FieldPanel("subject"),
    ]

    def save(self,*args,**kwargs):
        
        key = make_template_fragment_key(
            "contact_us"
        )

        key = make_template_fragment_key(
            "contact_us_landing"
        )
        cache.delete(key)
        return super().save(*args,**kwargs)
    
