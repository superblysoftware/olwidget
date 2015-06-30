from django import forms
from django.contrib import admin

from olwidget.admin import GeoModelAdmin
from olwidget.fields import MapField, EditableLayerField, InfoLayerField

from .models import Country, EnergyVortex, AlienActivity, Tree, Nullable, GoogProjModel


class TestAdminForm(forms.ModelForm):
    boundary = MapField([
        EditableLayerField({
            'geometry': 'polygon', 'name': 'boundary', 'is_collection': True
        }),
        InfoLayerField([['SRID=4326;POINT (0 0)', 'Of Interest']], {
            'name': 'Test'
        }),
    ], {
        'overlay_style': {'fill_color': '#00ff00'}
    }, template='olwidget/admin_olwidget.html')

    def clean(self):
        self.cleaned_data['boundary'] = self.cleaned_data['boundary'][0]
        return self.cleaned_data

    class Meta:
        model = Country
        exclude = ()


class CountryAdmin(GeoModelAdmin):
    form = TestAdminForm


# Custom multi-layer map with a few options.
class EnergyVortexAdmin(GeoModelAdmin):
    options = {
        'layers': ['osm.osmarender', 'osm.mapnik', 'yahoo.map'],
        'overlay_style': {
            'fill_color': '#ff9c00',
            'stroke_color': '#ff9c00',
            'fill_opacity': 0.7,
            'stroke_width': 4,
        },
        'default_lon': -111.7578,
        'default_lat': 34.87,
        'default_zoom': 15,
        'hide_textarea': False,
    }
    maps = (
        (('nexus', 'lines_of_force'), None),
    )


# Cluster changelist map
class TreeAdmin(GeoModelAdmin):
    list_map_options = {
        'cluster': True,
        'cluster_display': 'list',
        'map_div_style': {'width': '300px', 'height': '200px'},
        'default_zoom': 15,
    }
    list_map = ['location']
    maps = (
        (('location', 'root_spread'), {
            'default_lon': -71.08717,
            'default_lat': 42.36088,
            'default_zoom': 18,
        }),
    )


# Mixing default options and per-map options, also using changelist map
class AlienActivityAdmin(GeoModelAdmin):
    options = {
        'default_lon': -104.5185,
        'default_lat': 33.3944,
        'default_zoom': 12,
    }
    maps = (
        (('landings',), { 
            'overlay_style': { 
                'fill_color': '#00ff00',
                'stroke_color': '#00ff00',
            },
        }),
        (('strange_lights', 'chemtrails'), { 
            'overlay_style': {
                'fill_color': '#ffffff',
                'stroke_color': '#ccffcc',
                'stroke_width': 4,
            },
            'layers': ['osm.mapnik'],
        }),
    )
    list_map_options = {
        'cluster': True,
        'cluster_display': 'list',
        'map_div_style': {'width': '300px', 'height': '200px'},
    }
    list_map = ['landings']


class NullableAdmin(GeoModelAdmin):
    list_map_options = {
        'cluster': True,
        'cluster_display': 'list',
        'map_div_style': {'width': '300px', 'height': '200px'},
    }
    list_map = ['location']


class GoogProjAdmin(GeoModelAdmin):
    options = {
        'map_options': {
            'projection': 'EPSG:900913',
            'display_projection': 'EPSG:900913',
        },
        'hide_textarea': False,
    }


# Default map
# admin.site.register(Country, GeoModelAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(EnergyVortex, EnergyVortexAdmin)
admin.site.register(Tree, TreeAdmin)
admin.site.register(AlienActivity, AlienActivityAdmin)
admin.site.register(Nullable, NullableAdmin)
admin.site.register(GoogProjModel, GoogProjAdmin)
