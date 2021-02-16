from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from streams import blocks
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks as wagtail_blocks
from home.models import new_table_options
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key


class FlexPage(Page):
    parent_page_types = ["home.HomePage","flex.FlexPage"]
    class Meta:
        verbose_name = "Flex (misc) page"
        verbose_name_plural = "Flex (misc) pages"


#Declare the Stream Field
    body = StreamField([
        ('title', blocks.TitleBlock()),
        ('cards', blocks.CardsBlock()),
        ('images', blocks.ImageAndTextBlock()),
        ('cta', blocks.CallToActionBlock()),
        ("testimonials", SnippetChooserBlock(
            target_model = "testimonials.Testimonial",
            template = "streams/testimonial_block.html",
        )),
        ("table", blocks.PricingTableBlock(
            table_options = new_table_options
        )),
        ('rich_text', wagtail_blocks.RichTextBlock(
            template = "streams/simple_richtext_block.html"
        )),
        ('large_image', ImageChooserBlock(
            template = "streams/large_image_block.html",
            help_text = "This image will be cropped 1080px by 900px"
        ))
        #('new_richtext', blocks.NewRichTextBlock())
    ], null = True, blank = True)

    content_panels = Page.content_panels + [
        StreamFieldPanel("body")
    ]

    def save(self,*args,**kwargs):

        key = make_template_fragment_key(
            "flex_page",
            [self.id]
        )

        cache.delete(key)
        return super().save(*args,**kwargs)