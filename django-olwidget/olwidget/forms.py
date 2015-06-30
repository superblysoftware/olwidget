from django import forms
from django.contrib.gis.forms.fields import GeometryField
from django.utils import six

from olwidget.widgets import Map, BaseVectorLayer, EditableLayer
from olwidget.fields import MapField
from olwidget import utils

__all__ = ('MapModelForm', )


class BaseMapModelForm(forms.models.BaseModelForm):
    """
    ModelForm type that uses olwidget maps for geometry fields.  Multiple
    fields can be edited in a single map -- to do this, specify a property
    "maps" of the inner Meta class which lists fields and map options:

    class MyMapModelForm(MapModelForm):
        class Meta:
            model = MyModel
            maps = (
                (('geom1', 'geom2'), {'layers': ['google.streets]}), 
                (('geom3',), None), 
                ...
            ) 
    """
    def __init__(self, *args, **kwargs):
        super(BaseMapModelForm, self).__init__(*args, **kwargs)
        fix_initial_data(self.initial, self.initial_data_keymap)

    def clean(self):
        super(BaseMapModelForm, self).clean()
        fix_cleaned_data(self.cleaned_data, self.initial_data_keymap)
        return self.cleaned_data


class MapModelFormOptions(forms.models.ModelFormOptions):
    def __init__(self, options=None):
        super(MapModelFormOptions, self).__init__(options)
        self.maps = getattr(options, 'maps', None)
        if not self.maps:
            self.maps = getattr(options, 'options', None)
        self.default_field_class = getattr(options, 'default_field_class', None)
        self.template = getattr(options, 'template', None)


class MapModelFormMetaclass(type):
    """ 
    Metaclass for map-containing ModelForm widgets.  The implementation is
    mostly copied from Django's ModelFormMetaclass, but we change the
    hard-coded parent class name and add our map field processing parts.
    """
    def __new__(mcs, name, bases, attrs):
        formfield_callback = attrs.pop(
            'formfield_callback', lambda f, **kwargs: f.formfield(**kwargs))
        try:
            parents = [b for b in bases if issubclass(b, MapModelForm)]
        except NameError:
            # We are defining MapModelForm itself.
            parents = None
        declared_fields = forms.forms.get_declared_fields(bases, attrs, False)
        new_class = super(MapModelFormMetaclass, mcs).__new__(
            mcs, name, bases, attrs)
        if not parents:
            return new_class

        if 'media' not in attrs:
            new_class.media = forms.widgets.media_property(new_class)
        opts = new_class._meta = MapModelFormOptions(
            getattr(new_class, 'Meta', None))
        if opts.model:
            # If a model is defined, extract form fields from it.
            fields = forms.models.fields_for_model(
                opts.model, opts.fields, opts.exclude, opts.widgets,
                formfield_callback)

            # Override default model fields with any custom declared ones
            # (plus, include all the other declared fields).
            fields.update(declared_fields)
        else:
            fields = declared_fields

        # Transform base fields by extracting types mentioned in 'maps'
        initial_data_keymap = apply_maps_to_modelform_fields(
            fields, opts.maps, default_field_class=opts.default_field_class,
            default_template=opts.template)

        new_class.initial_data_keymap = initial_data_keymap
        new_class.declared_fields = declared_fields
        new_class.base_fields = fields
        return new_class


class MapModelForm(BaseMapModelForm):
    __metaclass__ = MapModelFormMetaclass


def fix_initial_data(initial, initial_data_keymap):
    """ 
    Take a dict like this as `initial`:
    { 'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}
    and a dict like this as `initial_data_keymap`:
    { 'newkey1': ['key1', 'key2'], 'newkey2': ['key3']}
    and remap the initial dict to have this form:
    { 'newkey1': ['val1', 'val2'], 'newkey2': ['val3']}

    Used for rearranging initial data in fields to match declared maps.
    """
    if initial:
        for dest, sources in six.iteritems(initial_data_keymap):
            data = [initial.pop(s, None) for s in sources]
            initial[dest] = data
    return initial


def fix_cleaned_data(cleaned_data, initial_data_keymap):
    for group, keys in six.iteritems(initial_data_keymap):
        if group in cleaned_data:
            vals = cleaned_data.pop(group)
            if isinstance(vals, (list, tuple)):
                for key, val in zip(keys, vals):
                    cleaned_data[key] = val
            else:
                cleaned_data[keys[0]] = vals
    return cleaned_data


def apply_maps_to_modelform_fields(fields, maps, default_options=None, 
                                   default_template=None, default_field_class=None):
    """
    Rearranges fields to match those defined in ``maps``. ``maps`` is a list
    of [field_list, options_dict] pairs.  For each pair, a new map field is
    created that contains all the fields in ``field_list``.
    """
    if default_field_class is None:
        default_field_class = MapField
    map_field_names = (name for name, field in six.iteritems(fields)
                       if isinstance(field, (MapField, GeometryField)))
    if not maps:
        maps = [((name,),) for name in map_field_names]
    elif isinstance(maps, dict):
        maps = [(map_field_names, maps)]

    default_options = utils.get_options(default_options)
    initial_data_keymap = {}

    for map_definition in maps:
        field_list = map_definition[0]
        options = {}
        template = default_template

        if len(map_definition) > 1:
            options = map_definition[1]
        if len(map_definition) > 2:
            template = map_definition[2]
        
        map_name = '_'.join(field_list)
        field = None
        layer_fields = []
        move_to_end = False
        initial_data_keymap[map_name] = []

        for field_name in six.iterkeys(fields):
            if field_name in field_list:
                field = fields.pop(field_name)
                initial_data_keymap[map_name].append(field_name)

                if not isinstance(field.widget, (Map, BaseVectorLayer)):
                    field.widget = EditableLayer(options=utils.options_for_field(field))
                layer_fields.append(field)

                # Placeholder
                fields.setdefault(map_name)

                # Don't start moving to the end until the first pop
                move_to_end = True
            elif move_to_end:
                fields.move_to_end(field_name)

        if isinstance(field, MapField):
            fields[map_name] = field
        else:
            map_opts = {}
            map_opts.update(default_options)
            map_opts.update(options or {})
            fields[map_name] = default_field_class(
                layer_fields, map_opts, layer_names=field_list, label=', '.join(
                    map(forms.forms.pretty_name, field_list)
                ), template=template)
    return initial_data_keymap
