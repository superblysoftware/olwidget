from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Country(models.Model):
    name = models.CharField(max_length=255)
    boundary = models.MultiPolygonField()
    about = models.TextField()

    objects = models.GeoManager()

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class EnergyVortex(models.Model):
    name = models.CharField(max_length=255)
    nexus = models.PointField()
    lines_of_force = models.MultiLineStringField()

    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Energy vortex')
        verbose_name_plural = _('Energy vortices')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AlienActivity(models.Model):
    incident_name = models.CharField(max_length=255)
    landings = models.MultiPointField()
    strange_lights = models.GeometryCollectionField()
    chemtrails = models.MultiLineStringField()

    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Alien activity')
        verbose_name_plural = _('Alien activities')

    def __str__(self):
        return self.incident_name


@python_2_unicode_compatible
class Tree(models.Model):
    location = models.PointField()
    root_spread = models.PolygonField()
    species = models.CharField(max_length=255)

    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Tree')
        verbose_name_plural = _('Trees')

    def __str__(self):
        return self.species


@python_2_unicode_compatible
class Nullable(models.Model):
    location = models.PointField(null=True, blank=True)

    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Nullable')
        verbose_name_plural = _('Nullables')

    def __str__(self):
        return '{0}'.format(self.location)


class GoogProjModel(models.Model):
    point = models.PointField(srid=900913)

    objects = models.GeoManager()

    class Meta:
        verbose_name = _('Goog Proj Model')
        verbose_name_plural = _('Goog Proj Models')
