from spotseeker_restclient.dao import SPOTSEEKER_DAO
from spotseeker_restclient.exceptions import DataFailureException
from spotseeker_restclient.models.spot import Spot, SpotAvailableHours, \
    SpotExtendedInfo, SpotImage, SpotType
from spotseeker_restclient.dao_implementation.spotseeker import File
import json
from django.utils.dateparse import parse_datetime, parse_time
from urllib import urlencode


class Spotseeker(object):

    def get_spot_by_id(self, spot_id):
        url = "/api/v1/spot/%s" % spot_id
        dao = SPOTSEEKER_DAO()
        if isinstance(dao._getDAO(), File):
            resp = dao.getURL(url, {})
            content = resp.data
        else:
            resp, content = dao.getURL(url, {})

        if resp.status != 200:
            raise DataFailureException(url, resp.status, content)

        return self._spot_from_data(json.loads(content))

    def search_spots(self, query_tuple):
        """
        Returns a list of spots matching the passed parameters.
        """

        dao = SPOTSEEKER_DAO()
        url = "/api/v1/spot?" + urlencode(query_tuple)
        if isinstance(dao._getDAO(), File):
            resp = dao.getURL(url, {})
            content = resp.data
        else:
            resp, content = dao.getURL(url, {})

        if resp.status != 200:
            raise DataFailureException(url, resp.status, content)

        results = json.loads(content)

        spots = []
        for res in results:
            spots.append(self._spot_from_data(res))

        return spots

    def _spot_from_data(self, spot_data):
        spot = Spot()

        spot.spot_id = spot_data["id"]
        spot.name = spot_data["name"]
        spot.uri = spot_data["uri"]
        spot.latitude = spot_data["location"]["latitude"]
        spot.longitude = spot_data["location"]["longitude"]
        spot.height_from_sea_level = \
            spot_data["location"]["height_from_sea_level"]
        spot.building_name = spot_data["location"]["building_name"]
        spot.building_description = spot_data["location"].get("description",
                                                              None)
        spot.floor = spot_data["location"]["floor"]
        spot.room_number = spot_data["location"]["room_number"]
        spot.capacity = spot_data["capacity"]
        spot.display_access_restrictions = \
            spot_data["display_access_restrictions"]
        spot.organization = spot_data["organization"]
        spot.manager = spot_data["manager"]
        spot.etag = spot_data["etag"]
        spot.external_id = spot_data["external_id"]

        spot.last_modified = parse_datetime(spot_data["last_modified"])
        spot.spot_types = self._spot_types_from_data(spot_data["type"])

        spot.spot_availability = \
            self._spot_availability_from_data(spot_data["available_hours"])
        spot.images = self._spot_images_from_data(spot_data["images"])
        spot.extended_info = \
            self._extended_info_from_data(spot_data["extended_info"])

        return spot

    def _spot_types_from_data(self, type_data):
        spot_types = []
        for spot_type in type_data:
            spot_types.append(SpotType(name=spot_type))
        return spot_types

    def _spot_availability_from_data(self, avaliblity_data):
        availability = []

        for day in avaliblity_data:
            for hours in avaliblity_data[day]:
                available_hours = SpotAvailableHours()
                available_hours.day = day
                available_hours.start_time = parse_time(hours[0])
                available_hours.end_time = parse_time(hours[1])
                availability.append(available_hours)
        return availability

    def _spot_images_from_data(self, image_data):
        images = []

        for image in image_data:
            spot_image = SpotImage()
            spot_image.image_id = image["id"]
            spot_image.url = image["url"]
            spot_image.description = image["description"]
            spot_image.display_index = image["display_index"]
            spot_image.content_type = image["content-type"]
            spot_image.width = image["width"]
            spot_image.height = image["height"]
            spot_image.creation_date = parse_datetime(image["creation_date"])
            spot_image.modification_date = \
                parse_datetime(image["modification_date"])
            spot_image.upload_user = image["upload_user"]
            spot_image.upload_application = image["upload_application"]
            spot_image.thumbnail_root = image["thumbnail_root"]

            images.append(spot_image)

        return images

    def _extended_info_from_data(self, info_data):
        extended_info = []

        for attribute in info_data:
            spot_extended_info = SpotExtendedInfo(key=attribute,
                                                  value=info_data[attribute])
            extended_info.append(spot_extended_info)
        return extended_info
