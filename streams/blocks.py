from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from django import forms
from wagtail.contrib.table_block.blocks import TableBlock

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
# Create your models here.
class TitleBlock(blocks.StructBlock):

    title = blocks.CharBlock(
        required = True,
        help_text = "This is a Struct Block",
    )

    class Meta:
        template = "streams/title_block.html" #Template (HTML) directory
        icon = "edit"
        help_text = "Centered text to display on the page"
        label = "Title"

class LinkValue(blocks.StructValue):
    # This is additional logic for the links #

    def link(self) -> str:
        internal_page = self.get("internal_page")
        external_page = self.get("external_page")
        if internal_page:
            return internal_page.url
        elif external_page:
            return external_page
        else:
            return ""


class Link(blocks.StructBlock):

    link_title = blocks.TextBlock(
        max_length = 100
    )

    internal_page = blocks.PageChooserBlock(
        help_text = "Enter a Link",
        required = False
    )
    external_page = blocks.CharBlock(
        help_text = "Enter an external page",
        required = False
    )

    class Meta:
        value_class = LinkValue

    #def clean(self, value):
    #    internal_page = value.get("internal_page")
    #    external_page = value.get("external_page")
    #    if internal_page and external_page:
    #        raise ValidationError({
    #            'internal_page': ValidationError("Please enter only an internal page or an external page"),
    #            'external_page': ValidationError("Please enter only an internal page or an external page")
    #        })
    #    elif not internal_page and not external_page:
    #        raise ValidationError({
    #            'internal_page': ValidationError("Please an internal or external page must be submit"),
    #            'external_page': ValidationError("Please an internal or external page must be submit")
    #        })
     #   return super().clean(value)

    #def clean(self, value):
    #   internal_page = value.get("internal_page")
    #    external_page = value.get("external_page")
    #    errors = {}
    #
    #    if internal_page and external_page:
    #        errors['internal_page'] = ErrorList(["Only one link can be submitted at the time, please submit only one link"])
    #        errors['external_page'] = ErrorList(["Only one link can be submitted at the time, please submit only one link"])
    #    if not internal_page and not external_page:
    #        errors['internal_page'] = ErrorList(["There's no link submitted, please submit only one link"])
    #        errors['external_page'] = ErrorList(["There's no link submitted, please submit only one link"])
    #    if errors:
    #        raise ValidationError("Valid the submitted link: ", params=errors)
    #
    #    return super().clean(value)

class Card(blocks.StructBlock):

    title = blocks.CharBlock(
                help_text = "Bold text title for this card, max length is 100 characters",
                max_length = 100
    )
    text = blocks.TextBlock(
                max_length = 500,
                help_text = "Paragraph text for this card, max length is 500 characterss"
    )
    image = ImageChooserBlock(
                help_text = "This image will be automatically cropped to 570px by 370px"
    )

    link = Link(help_text = "Enter a Link or an external Page")



class CardsBlock(blocks.StructBlock):

    cards = blocks.ListBlock(
        Card()
    )

    class Meta:
        template = 'streams/card_block.html'
        icon = "image"
        label = "Card"


class RadioSelectorBlock(blocks.ChoiceBlock):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.field.widget = forms.RadioSelect(
            choices = self.field.widget.choices
        )

class ImageAndText(blocks.StructBlock):
    image = ImageChooserBlock(
        required = True,
        help_text = "Image will be cropped 570px by 370px"
    )
    image_alignment = RadioSelectorBlock(
        choices = (
            ('left', 'Image to the left'),
            ('right', 'Image to the right')
        ),
        default = "left",
        help_text = "Image on the left with text on the right, Image in the right with text on the left"
    )
    title = blocks.CharBlock(
        max_length = 50,
        default = "Title",
        help_text = "Max length is 50 characters..."
    )
    text = blocks.CharBlock(
        max_length = 500,
        help_text = "Max length is 500 characters...",
        required = False
    )
    link = Link()

class ImageAndTextBlock(blocks.StructBlock):

    imgtexts = blocks.ListBlock(
        ImageAndText()
    )

    class Meta:
        template = 'streams/image_and_text_block.html'
        icon = "image"
        label = "Image and Text"

class CallToActionBlock(blocks.StructBlock):

    title = blocks.CharBlock(
        max_length = 200,
        help_text = "Max Characters for the title is 200 characters"
    )

    link = Link()

    class Meta:
        template = "streams/call_to_action_block.html"
        icon = 'image'
        label = "Call to Action Block"


class PricingTableBlock(TableBlock):

    class Meta:
        template = "streams/pricing_table_block.html"
        icon = "table"
        label = "Table block"


#class NewRichTextBlock(blocks.StructBlock):
#
#    title = blocks.CharBlock(
#        max_length = 50,
#       help_text = "Rich Text Title"
#    )
#   context = blocks.RichTextBlock()
#
#    class Meta:
#        template = "streams/new_richtext_block.html"
#        icon = "edit"
#        label = "New Rich Text"