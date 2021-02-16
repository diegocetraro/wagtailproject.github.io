from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.edit_handlers import PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from django.core.exceptions import ValidationError

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
# Create your models here.

#*************App for Service Listing Page******************
class ServiceListingPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["services.ServicePage"]
    max_count = 1
    template = "services/service_listing_page.html"
    subtitle = models.TextField(
        blank = True,
        max_length = 500,
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['card_content'] = ServicePage.objects.live().public()
        return context

    def save(self, *args,**kwargs):

        key = make_template_fragment_key(
            "service_listing_page",
            [self.id]
        )
        cache.delete(key)
        return super().save(*args,**kwargs)

#*************App for Service Listing Page******************


#*************App for Service Page*******************
class ServicePage(Page):
    parent_page_types = ["services.ServiceListingPage"]
    subpage_types = []
    template = "services/service_page.html"
    description = models.TextField(
        blank = True,
        max_length = 500,
    )

    internal_page = models.ForeignKey(
        'wagtailcore.Page',
        blank = True,
        null = True,
        related_name = "+",
        help_text = 'Select an internal wagtail page',
        on_delete = models.SET_NULL,
    )

    external_page = models.URLField(
        blank = True,
    )

    service_listing_page = models.ForeignKey(
        'wagtailcore.Page',
        blank = True,
        null = True,
        related_name ="+",
        on_delete = models.SET_NULL
    )

    button_text = models.CharField(
        blank = True,
        max_length = 50,
    )
    service_image = models.ForeignKey(
        'wagtailimages.Image',
        null = True,
        blank = False,
        on_delete = models.SET_NULL,
        help_text = "This image will be  used for service listing page and will be cropped to 570px by 370px",
        related_name = "+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        PageChooserPanel("internal_page"),
        FieldPanel("external_page"),
        PageChooserPanel("service_listing_page"),
        FieldPanel("button_text"),
        ImageChooserPanel("service_image")
    ]

    def link(self) -> str:
        if self.internal_page:
            return self.internal_page.url
        elif self.external_page:
            return self.external_page
        else:
            return ""


    def save(self, *args,**kwargs):

        key = make_template_fragment_key(
            "service_page",
            [self.id]
        )
        cache.delete(key)
        return super().save(*args,**kwargs)

#*************App for Service Page*******************



# *************Validation Error code (Internal_Page or External_Page)***************
    def clean(self):
        super().clean()

        if self.internal_page and self.external_page:
            raise ValidationError({
                'internal_page': ValidationError("Please enter only an internal page or an external page"),
                'external_page': ValidationError("Please enter only an internal page or an external page")
            })
        if not self.internal_page and not self.external_page:
            raise ValidationError({
                'internal_page': ValidationError("Please an internal or external page must be submit"),
                'external_page': ValidationError("Please an internal or external page must be submit")
            })

# *************Validation Error code (Internal_Page or External_Page)***************
