from django.contrib import admin
from .models import (
    About,
    AboutImage,
    AboutMember,
    AboutDate,
    Booking,
    Event,
    EventImage,
    Info,
    InfoImage,
    Testimonial,
    Portfolio,
    NewsList
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
class BookingAdmin(admin.ModelAdmin):
    list_display        = ('event','booked_at','name','phone','email','abo','status','pay_till')
    list_filter         = ('event','status','abo')
    search_fields       = ('name','email','event')

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

class NewsAdmin(admin.ModelAdmin):
    list_display        = ('email','active','inscribed_at')
    list_filter         = ('active',)


admin.site.register(Info, InfoAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(NewsList,NewsAdmin)
admin.site.register(AboutDate)
admin.site.register(AboutMember)
admin.site.register(Testimonial)
admin.site.register(Portfolio, PortfolioAdmin)
