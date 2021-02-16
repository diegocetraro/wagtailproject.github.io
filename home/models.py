from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock

#Call the classes: TitleBlock and blocks from Streams.block
from streams.blocks import TitleBlock, CardsBlock, ImageAndTextBlock, CallToActionBlock, PricingTableBlock
from streams import blocks

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

new_table_options = {
    'minSpareRows': 0,
    'startRows': 4,
    'startCols': 4,
    'colHeaders': False,
    'rowHeaders': False,
    'contextMenu': [
        'row_above',
        'row_below',
        '---------',
        'col_left',
        'col_right',
        '---------',
        'remove_row',
        'remove_col',
        '---------',
        'undo',
        'redo'
    ],
    'editor': 'text',
    'stretchH': 'all',
    'height': 108,
    'renderer': 'text',
    'autoColumnSize': False,
}


class HomePage(Page):
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["flex.FlexPage", "services.ServiceListingPage","contacts.ContactPage"]
    max_count = 1
    
    lead_text = models.CharField(
        max_length = 140,
        blank = True,
        help_text = "Subsequent text after the banner title idk some other stuff ok?",
    )

    button = models.ForeignKey(
        'wagtailcore.Page',
        blank = True,
        null = True,
        on_delete = models.SET_NULL,
        related_name = '+',
        help_text = "Page Chooser Panel"
    )

    button_text = models.CharField(
        max_length = 50,
        blank = False,
        help_text = "The Button Text",
    )

    banner_background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank = False,
        null = True,
        related_name = '+',
        help_text = 'The banner background image',
        on_delete = models.SET_NULL,
    )

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
        ))
    ], null = True, blank = True)

    content_panels = Page.content_panels + [
        FieldPanel("lead_text"),    
        PageChooserPanel("button"),
        FieldPanel("button_text"),
        ImageChooserPanel("banner_background_image"),
        StreamFieldPanel("body"), #Add the stream field to content Panel
    ]

    #*********Remove Caching every time the page gets saved**************
    
    def save(self, *args, **kwargs):

        key = make_template_fragment_key(
            "home_page_streams",
            [self.id], #This value is a list
        )

        cache.delete(key)

        return super().save(*args,**kwargs)

    #*********Remove Caching every time the page gets saved**************
