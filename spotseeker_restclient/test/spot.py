from django.test import TestCase
from spotseeker_restclient.spotseeker import Spotseeker
from spotseeker_restclient.exceptions import DataFailureException
from django.utils.dateparse import parse_datetime, parse_time
from django.test.utils import override_settings

DAO = "spotseeker_restclient.dao_implementation.spotseeker.File"


@override_settings(SPOTSEEKER_DAO_CLASS=DAO)
class SpotseekerTest(TestCase):

    def test_get_spot(self):
        spot_client = Spotseeker()

        spot_data = spot_client.get_spot_by_id('123')

        self.assertEqual(spot_data.spot_id, "123")
        self.assertEqual(spot_data.name, "Test Spot")
        self.assertEqual(spot_data.uri, "/api/v1/spot/123")
        self.assertEqual(spot_data.latitude, 3.60)
        self.assertEqual(spot_data.longitude, 1.34)
        self.assertEqual(spot_data.height_from_sea_level, 0.10)
        self.assertEqual(spot_data.building_name, "Test Building")
        self.assertEqual(spot_data.floor, 0)
        self.assertEqual(spot_data.room_number, "456")
        self.assertEqual(spot_data.capacity, 0)
        self.assertEqual(spot_data.display_access_restrictions, "none")
        self.assertEqual(spot_data.organization, "Test Org")
        self.assertEqual(spot_data.manager, "Mr Test Org")
        self.assertEqual(spot_data.etag, "686897696a7c876b7e")
        self.assertEqual(spot_data.external_id, "asd123")
        self.assertEqual(spot_data.last_modified,
                         parse_datetime("2012-07-13T05:00:00+00:00"))

        self.assertEqual(len(spot_data.images), 1)
        self.assertEqual(spot_data.images[0].image_id, "1")
        self.assertEqual(spot_data.images[0].url,
                         "/api/v1/spot/123/image/1")
        self.assertEqual(spot_data.images[0].content_type, "image/jpeg")
        self.assertEqual(spot_data.images[0].width, 0)
        self.assertEqual(spot_data.images[0].height, 0)
        self.assertEqual(spot_data.images[0].creation_date,
                         parse_datetime("Sun, 06 Nov 1994 08:49:37 GMT"))
        self.assertEqual(spot_data.images[0].modification_date,
                         parse_datetime("Mon, 07 Nov 1994 01:49:37 GMT"))
        self.assertEqual(spot_data.images[0].upload_user,
                         "user name")
        self.assertEqual(spot_data.images[0].upload_application,
                         "application name")
        self.assertEqual(spot_data.images[0].thumbnail_root,
                         "/api/v1/spot/123/image/1/thumb")
        self.assertEqual(spot_data.images[0].description,
                         "Information about the image")
        self.assertEqual(spot_data.images[0].display_index, 0)

        self.assertEqual(len(spot_data.spot_availability), 7)

    def test_spot_items(self):
        spot_client = Spotseeker()
        spot_data = spot_client.get_spot_by_id('1')
        self.assertEqual(len(spot_data.items), 2)
        item1 = spot_data.items[0]
        self.assertEqual(item1.item_id, 796)
        self.assertEqual(item1.name, "C-19074")
        self.assertEqual(item1.category, "Digital Camera")
        self.assertEqual(item1.subcategory, "")
        self.assertEqual(len(item1.images), 1),
        self.assertEqual(item1.images[0].image_id, 1),

    def test_bad_spot(self):
        spot_client = Spotseeker()
        self.assertRaises(DataFailureException,
                          spot_client.get_spot_by_id, 999)

    def test_search_spots(self):
        """ Tests search_spots function with mock data provided in the
            file named : spot?limit=5&center_latitude=47.653811&
                    center_longitude=-122.307815&distance=100000&
                    fuzzy_hours_start=Tuesday%2C05%3A00&fuzzy_hours_end=
                    Tuesday%2C11%3A00&extended_info%3Aapp_type=food
            tests mock data is accessible if filename matches order
            of query_tuple passed.
        """

        spot_client = Spotseeker()
        query_tuple = [
                    ('limit', 5), ('center_latitude', u'47.653811'),
                    ('center_longitude', u'-122.307815'),
                    ('distance', 100000),
                    ('fuzzy_hours_start', 'Tuesday,05:00'),
                    ('fuzzy_hours_end', 'Tuesday,11:00'),
                    ('extended_info:app_type', 'food')]

        spot_data_list = spot_client.search_spots(query_tuple)
        spot_data = spot_data_list[0]

        self.assertEqual(len(spot_data_list), 5)
        self.assertEqual(spot_data.spot_id, 40)
        self.assertEqual(spot_data.name, "TestSpot1")
        self.assertEqual(spot_data.uri, "/api/v1/spot/40")
        self.assertEqual(spot_data.latitude, 47)
        self.assertEqual(spot_data.longitude, -12)
        self.assertEqual(spot_data.height_from_sea_level, 0.10)
        self.assertEqual(spot_data.building_name, "TestBuilding")
        self.assertEqual(spot_data.capacity, 0)
        self.assertEqual(spot_data.organization, "Test Org")
        self.assertEqual(spot_data.manager, "Test Manager")
        self.assertEqual(spot_data.etag, "123456789")
        self.assertEqual(spot_data.last_modified,
                         parse_datetime("2012-07-13T05:00:00+00:00"))

        self.assertEqual(len(spot_data.images), 1)
        self.assertEqual(spot_data.images[0].image_id, "1")
        self.assertEqual(spot_data.images[0].url,
                         "/api/v1/spot/123/image/1")
        self.assertEqual(spot_data.images[0].content_type, "image/jpeg")
        self.assertEqual(spot_data.images[0].width, 0)
        self.assertEqual(spot_data.images[0].height, 0)
        self.assertEqual(spot_data.images[0].creation_date,
                         parse_datetime("Sun, 06 Nov 1994 08:49:37 GMT"))
        self.assertEqual(spot_data.images[0].modification_date,
                         parse_datetime("Mon, 07 Nov 1994 01:49:37 GMT"))
        self.assertEqual(spot_data.images[0].upload_user,
                         "user name")
        self.assertEqual(spot_data.images[0].upload_application,
                         "application name")
        self.assertEqual(spot_data.images[0].thumbnail_root,
                         "/api/v1/spot/123/image/1/thumb")
        self.assertEqual(spot_data.images[0].description,
                         "Information about the image")
        self.assertEqual(spot_data.images[0].display_index, 0)

        self.assertEqual(len(spot_data.spot_availability), 5)

    def test_building_list(self):
        spot_client = Spotseeker()
        buildings = spot_client.get_building_list("seattle")
        self.assertEqual(len(buildings), 43)

    def test_get_all_spots(self):
        spot_client = Spotseeker()
        spots = spot_client.all_spots()
        self.assertEqual(len(spots), 3)
