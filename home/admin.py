from django.contrib import admin
from .models import (
    About,
    AboutImage,
    AboutMember,
    AboutDate,
    Event,
    EventImage,
    Info,
    InfoImage,
    Testimonial,
    Portfolio,
)

class AboutImageInline(admin.StackedInline):
    model               = AboutImage
    extra               = 1
    can_delete          = True
    show_change_link    = True

class AboutAdmin(admin.ModelAdmin):
    inlines             = [
        AboutImageInline,
             ]

class PortfolioAdmin(admin.ModelAdmin):
    list_display        = ('order','text','upload')

class EventImageInline(admin.StackedInline):
    model               = EventImage
    extra               = 1
    can_delete          = True
    show_change_link    = True

class EventAdmin(admin.ModelAdmin):
    list_display        = ('title','city','datestart','dateend','slug')
    list_filter         = ('cat','level','city')
    search_fields       = ('title','datestart','dateend')
    inlines             = [
        EventImageInline,
             ]
class InfoImageInline(admin.StackedInline):
    model               = InfoImage
    extra               = 1
    can_delete          = True
    show_change_link    = True

class InfoAdmin(admin.ModelAdmin):
    list_display        = ('title','slug')
    inlines             = [
        InfoImageInline,
    ]
admin.site.register(Info, InfoAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(AboutDate)
admin.site.register(AboutMember)
admin.site.register(Testimonial)
admin.site.register(Portfolio, PortfolioAdmin)
