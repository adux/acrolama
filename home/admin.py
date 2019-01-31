from django.contrib import admin
from .models import (
    About,
    AboutImage,
    AboutMember,
    AboutDate,
    Accounting,
    Booking,
    Event,
    EventImage,
    Faq,
    FaqValues,
    Info,
    InfoImage,
    NewsList,
    Portfolio,
    Teacher,
    Testimonial
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
    list_display        = ('event','booked_at','name','phone','email','abo','day','status')
    list_filter         = ('event','status','abo')
    search_fields       = ('name','email','event__title')

class PortfolioAdmin(admin.ModelAdmin):
    list_display        = ('order','text','upload')

class EventImageInline(admin.StackedInline):
    model               = EventImage
    extra               = 1
    can_delete          = True
    show_change_link    = True

class EventTeacherInline(admin.StackedInline):
    model               = Teacher
    extra               = 1
    can_delete          = True
    show_change_link    = True

class FaqAdmin(admin.ModelAdmin):
    list_display        = 'question', 'answer'


class AccountingInline(admin.StackedInline):
    model               = Accounting
    extra               = 1
    can_delete          = True

class EventAdmin(admin.ModelAdmin):
    list_display        = ('title','city','datestart','dateend','slug','published','registration')
    list_filter         = ('cat','level','city')
    search_fields       = ('title','datestart','dateend')
    inlines             = [
        EventImageInline,
        EventTeacherInline,
        AccountingInline,
             ]

class AccountingAdmin(admin.ModelAdmin):
    list_display        =('category','event','status','amount')
    search_fields       =('event','category','status')


class TeacherAdmin(admin.ModelAdmin):
    list_display        =('name','content')
    search_fields       =('name','content')


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


admin.site.register(About, AboutAdmin)
admin.site.register(AboutDate)
admin.site.register(AboutMember)
admin.site.register(Accounting,AccountingAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(NewsList,NewsAdmin)
admin.site.register(Testimonial)
admin.site.register(Portfolio, PortfolioAdmin)
