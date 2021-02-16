from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import RichTextField

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
# Create your models here.


@register_setting
class HourSettings(BaseSetting):

    hour = RichTextField(
        blank = True,
    )

    panels = [
        FieldPanel("hour")
    ]

    def save(self, *args, **kwargs):
        key = make_template_fragment_key(
            "footer_contact_settings"
        )
        cache.delete(key)
        return super().save(*args, **kwargs)

@register_setting
class ContactSettings(BaseSetting):

    text = RichTextField(
        blank = True,
    )

    panels = [
        FieldPanel("text")
    ]

    def save(self, *args, **kwargs):
        key = make_template_fragment_key(
            "footer_contact_settings"
        )
        cache.delete(key)
        return super().save(*args, **kwargs)

class SocialMediaSettings(blocks.StructBlock):

    social_name = blocks.CharBlock(
        max_length = 50,
        required = False,
        help_text = "Enter the name of the social media"
    ) 
   
    social_url = blocks.URLBlock(
        required = False,
        help_text = "Enter the URL of the social media"
    )

    social_img = ImageChooserBlock(
        required = False,
        help_text = "Enter image of the social media",
    )


@register_setting
class Social(BaseSetting):

    body = StreamField([
        ('social', SocialMediaSettings(
           template = "streams/socials.html"
        )),
    ])

    panels = [
        StreamFieldPanel("body")
    ]

    def save(self, *args,**kwargs):

        key = make_template_fragment_key("site_social")
        cache.delete(key)
        return super().save(*args,**kwargs)

@register_setting
class FooterCTASetting(BaseSetting):

    title = models.CharField(
        max_length = 50,
        blank = True,
        help_text = "CTA Settings Title",
    )

    text = RichTextField(
        blank = True,
    )
    
    page_name = models.CharField(
        max_length = 50,
        blank = True,
        help_text = "Contact Page Name",
    )

    contact = models.ForeignKey(
        'wagtailcore.Page',
        blank = True,
        null = True,
        related_name = "+",
        on_delete = models.SET_NULL,
    )



    panels = [
        FieldPanel("title"),
        FieldPanel("text"),
        FieldPanel("page_name"),
        PageChooserPanel("contact"),
    ]

    def save(self,*args,**kwargs):
        key = make_template_fragment_key(
            "footer_cta_settings_title"
        )
        key = make_template_fragment_key(
            "footer_cta_settings_texr"
        )
        key = make_template_fragment_key(
            "footer_cta_settings_page"
        )
        cache.delete(key)
        return super().save(*args,**kwargs)