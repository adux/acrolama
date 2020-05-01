from home.models import Info

def createInfoFromPolicy(instance):
    name = instance.name.replace(" ", "")
    try:
        get_info = Info.objects.get(slug = name)
    except Info.DoesNotExist:
        obj = Info()
        obj.title = instance.name
        obj.content = instance.description
        obj.slug = name
        obj.save()
        return obj
    else:
        get_info.update(title = instance.name)
        get_info.update(content = instance.description)
        get_info.update(slug = instance.slug)
        return get_info

