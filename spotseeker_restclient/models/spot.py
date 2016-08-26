from django.db import models


class SpotType(models.Model):
    """ The type of Spot.
    """
    name = models.SlugField(max_length=50)


class SpotAvailableHours(models.Model):
    """
    The hours a Spot is available, i.e. the open or closed hours for the
    building the spot is located in.
    """

    day = models.CharField(max_length=9)

    start_time = models.TimeField()
    end_time = models.TimeField()


class SpotExtendedInfo(models.Model):
    """
    Additional institution-provided metadata about a spot. If providing custom
    metadata, you should provide a validator for that data, as well.
    """
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=255)


class SpotImage(models.Model):
    """
    An image of a Spot. Multiple images can be associated with a Spot,
    and Spot objects have a 'Spot.spotimage_set' method that will return all
    SpotImage objects for the Spot.
    """

    image_id = models.IntegerField()
    url = models.CharField(max_length=255)
    description = models.CharField(max_length=200, blank=True)
    display_index = models.PositiveIntegerField(null=True, blank=True)
    content_type = models.CharField(max_length=40)
    width = models.IntegerField()
    height = models.IntegerField()
    creation_date = models.DateTimeField()
    modification_date = models.DateTimeField()
    upload_user = models.CharField(max_length=40)
    upload_application = models.CharField(max_length=100)


class Spot(models.Model):
    """ Represents a place for students to study.
    """
    spot_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=True)
    uri = models.CharField(max_length=255)
    thumbnail_root = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    height_from_sea_level = models.DecimalField(max_digits=11,
                                                decimal_places=8,
                                                null=True,
                                                blank=True)
    building_name = models.CharField(max_length=100, blank=True)
    floor = models.CharField(max_length=50, blank=True)
    room_number = models.CharField(max_length=25, blank=True)
    building_description = models.CharField(max_length=100, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    display_access_restrictions = models.CharField(max_length=200, blank=True)
    organization = models.CharField(max_length=50, blank=True)
    manager = models.CharField(max_length=50, blank=True)
    etag = models.CharField(max_length=40)
    last_modified = models.DateTimeField()
    external_id = models.CharField(max_length=100,
                                   null=True,
                                   blank=True,
                                   default=None,
                                   unique=True)


class SpotItem(models.Model):
    item_id = models.IntegerField()
    name = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)


class ItemImage(models.Model):
    image_id = models.IntegerField()
    description = models.CharField(max_length=200, blank=True)
    display_index = models.PositiveIntegerField(null=True, blank=True)
    width = models.IntegerField()
    height = models.IntegerField()
    content_type = models.CharField(max_length=40)
    creation_date = models.DateTimeField(auto_now_add=True)
    upload_user = models.CharField(max_length=40)
    upload_application = models.CharField(max_length=100)
