from wagtail.contrib.modeladmin.options import(
    ModelAdmin, modeladmin_register
)
from .models import Testimonial
# Register your models here.

@modeladmin_register
class TestimonialAdmin(ModelAdmin):

    model = Testimonial
    menu_label ="Testimonial"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    search_fields = ("quote", "attribution")
    list_display = ("quote","attribution")
