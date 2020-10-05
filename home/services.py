from home.models import Info


def create_info_from_policy(instance):
    name = instance.name.replace(" ", "")
    try:
        info = Info.objects.get(slug=name)
    except Info.DoesNotExist:
        obj = Info()
        obj.title = instance.name
        obj.content = instance.description
        obj.slug = name
        obj.save()
        return obj
    else:
        info.title = instance.name
        info.content = instance.description
        info.save()
        return info
