from dal.autocomplete import ModelSelect2, ModelSelect2Multiple
from django import forms
from django.utils.datastructures import MultiValueDict


class DynamicArrayWidget(forms.TextInput):

    template_name = "booking/dynamic_array.html"

    def get_context(self, name, value, attrs):
        context_value = value or [""]
        context = super().get_context(name, context_value, attrs)
        final_attrs = context["widget"]["attrs"]
        id_ = context["widget"]["attrs"].get("id")
        context["widget"]["is_none"] = value is None

        subwidgets = []
        for index, item in enumerate(context["widget"]["value"]):
            widget_attrs = final_attrs.copy()
            if id_:
                widget_attrs["id"] = "{id_}_{index}".format(id_=id_, index=index)
            widget = forms.TextInput()
            widget.is_required = self.is_required
            subwidgets.append(widget.get_context(name, item, widget_attrs)["widget"])

        context["widget"]["subwidgets"] = subwidgets
        return context

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
            return [value for value in getter(name) if value]
        except AttributeError:
            return data.get(name)

    def format_value(self, value):
        return value or []


class BootstrapedSelect2(ModelSelect2):
    def build_attrs(self, *args, **kwargs):
        """Set Bootraped default"""
        attrs = super(BootstrapedSelect2, self).build_attrs(*args, **kwargs)
        attrs['data-theme'] = 'bootstrap4'
        attrs['data-width'] = 'style'
        return attrs


class BootstrapedSelect2Multiple(ModelSelect2Multiple):
    def build_attrs(self, *args, **kwargs):
        """Set Bootraped default"""
        attrs = super(BootstrapedSelect2Multiple, self).build_attrs(*args, **kwargs)
        attrs['data-theme'] = 'bootstrap4'
        attrs['data-width'] = 'style'
        return attrs


class M2MSelect(forms.Select):
    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict)):
            return data.getlist(name)
        return data.get(name, None)
