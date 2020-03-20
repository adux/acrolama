from django.contrib import admin
from .models import (
    AboutImage,
    AboutTeam,
    AboutDate,
    Faq,
    Info,
    InfoImage,
    NewsList,
    Portfolio,
    Testimonial,
)


class AboutImageAdmin(admin.ModelAdmin):
    model = AboutImage
    can_delete = True
    show_change_link = True


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("order", "text")


class FaqAdmin(admin.ModelAdmin):
    list_display = "question", "answer"


class InfoImageInline(admin.StackedInline):
    model = InfoImage
    extra = 1
    can_delete = True
    show_change_link = True

class InfoAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    inlines = [InfoImageInline]


class NewsAdmin(admin.ModelAdmin):
    list_display = ("event", "image")


admin.site.register(AboutImage, AboutImageAdmin)
admin.site.register(AboutDate)
admin.site.register(AboutTeam)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(NewsList, NewsAdmin)
admin.site.register(Testimonial)
admin.site.register(Portfolio, PortfolioAdmin)
