from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    MultiFieldPanel,
    InlinePanel,
    FieldPanel,
    PageChooserPanel,
)
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

class MenuItem(Orderable):

    link_title = models.CharField(
        max_length = 50,
        blank = True
    )
    external_page = models.URLField(
        blank = True,
        max_length = 500
    )
    internal_link = models.ForeignKey(
        'wagtailcore.Page',
        null = True,
        blank = True,
        related_name = "+",
        on_delete = models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(
        default = False,
        blank = True,
    )

    panels = [
        FieldPanel("link_title"),
        FieldPanel("external_page"),
        PageChooserPanel("internal_link"),
        FieldPanel("open_in_new_tab")
    ]

    link_menu = ParentalKey("Menu", related_name="menu_items")
    
    def link(self) ->str:
        if self.internal_link:
            return self.internal_link.url
        elif self.external_page:
            return self.external_page
        else:
            return ""
        
    def validate_title(self) -> str:
        if self.link_title:
            return self.link_title
        elif not self.link_title:
            return ""


@register_snippet
class Menu(ClusterableModel):

    title = models.CharField(
        max_length = 100, 
    )
    slug = models.SlugField(
        max_length = 100,
        editable = True
    )
    panels = [
            FieldPanel("title"),
            FieldPanel("slug"),
            InlinePanel("menu_items", label="Menu Items")
        ]
    
    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):

        key = make_template_fragment_key(
            "site_header",
            [self.id]
        )

        key = make_template_fragment_key(
            "site_footer",
            [self.id]
        )

        key = make_template_fragment_key(
            "site_contact",
            [self.id]
        )

        cache.delete(key)
        return super().save(self,*args,**kwargs)

