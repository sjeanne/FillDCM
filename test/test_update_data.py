""" Data generation functions unit tests
"""

import unittest
from copy import deepcopy
import string
from filldcm import fill_dcm


class TestGenerates(unittest.TestCase):
    """ Test all function related to data generation
    """

    def test_update_data_values(self):
        """ Call to update_data() with input values. Only 'None' tags are updated with  a random value
        """
        input_values = {
            "tags": {
                "PatientName": "patient^name^complicated",
                "PatientID": "1234567890AZERTY",
                "PatientBirthDate": "20000101",
                "ReferringPhysicianName": None,
                "DeviceSerialNumber": None,
            },
            "tags_to_overwrite": None
        }

        updated_values = deepcopy(input_values)
        fill_dcm.update_data(updated_values)

        # Tags are not updated
        self.assertEqual(
            updated_values["tags"]["PatientName"], input_values["tags"]["PatientName"])
        self.assertEqual(
            updated_values["tags"]["PatientID"], input_values["tags"]["PatientID"])
        self.assertEqual(
            updated_values["tags"]["PatientBirthDate"], input_values["tags"]["PatientBirthDate"])
        # Tags have a value defined now
        self.assertIsNotNone(updated_values["tags"]["ReferringPhysicianName"])
        self.assertIsNotNone(updated_values["tags"]["DeviceSerialNumber"])

    def test_tags_to_overwrite_not_updated(self):
        """ Tags to overwrite are not updated
        """
        input_values = {
            "tags": None,
            "tags_to_overwrite": {
                "PatientID": "1234567890AZERTY",
                "PatientName": "patient^name^complicated"
            }
        }

        updated_values = deepcopy(input_values)
        fill_dcm.update_data(updated_values)

        # Tags shall not be updated
        self.assertEqual(input_values["tags_to_overwrite"]["PatientID"],
                         updated_values["tags_to_overwrite"]["PatientID"])
        self.assertEqual(input_values["tags_to_overwrite"]["PatientName"],
                         updated_values["tags_to_overwrite"]["PatientName"])

    def test_update_data_with_empty_input(self):
        """ Empty structure is passed, no exception are raised.
        """
        fill_dcm.update_data({"tags": None, "tags_to_overwrite": None})

    def test_update_data_vr_as(self):
        """ AS VR is managed, update_data() creates a value for AG tags
        """
        input_values = {
            "tags": {"PatientAge": None}, "tags_to_overwrite": None}
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["PatientAge"])

    def test_update_data_vr_ds(self):
        """ DS VR is managed, update_data() creates a value for DS tags
        """
        input_values = {
            "tags": {"PixelSpacing": None}, "tags_to_overwrite": None}
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["PixelSpacing"])

    def test_update_data_vr_dt(self):
        """ DT VR is managed, update_data() creates a value for DT tags
        """
        input_values = {
            "tags": {"AcquisitionDateTime": None}, "tags_to_overwrite": None}
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["AcquisitionDateTime"])

    def test_update_data_vr_is(self):
        """ IS VR is managed, update_data() creates a value for IS tags
        """
        input_values = {
            "tags": {"SeriesNumber": None}, "tags_to_overwrite": None}
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["SeriesNumber"])

    def test_update_data_vr_lt(self):
        """ LT VR is managed, update_data() creates a value for LT tags
        """
        input_values = {
            "tags": {"ImageComments": None}, "tags_to_overwrite": None}
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["ImageComments"])

    def test_update_data_vr_sh(self):
        """ SH VR is managed, update_data() creates a value for SH tags
        """
        input_values = {
            "tags": {"StationName": None}, "tags_to_overwrite": None}
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["StationName"])

    def test_update_data_vr_st(self):
        """ ST VR is managed, update_data() creates a value for ST tags
        """
        input_values = {
            "tags": {"InstitutionAddress": None}, "tags_to_overwrite": None}
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["InstitutionAddress"])

    def test_update_data_throw_vr_tm(self):
        """ TM VR is managed, update_data() creates a value for TM tags
        """
        input_values = {
            "tags": {"SeriesTime": None}, "tags_to_overwrite": None}
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["SeriesTime"])

    def test_update_data_throw_vr_ui(self):
        """ UI VR is managed, update_data() creates a value for UI tags
        """
        input_values = {
            "tags": {"DeviceUID": None}, "tags_to_overwrite": None}
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["DeviceUID"])

    def test_update_data_throw_vr_us(self):
        """ US VR is managed, update_data() creates a value for US tags
        """
        input_values = {
            "tags": {"Rows": None}, "tags_to_overwrite": None}
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["Rows"])

    def test_generate_personal_name(self):
        """ Test generate_personal_name()
        """
        pn = fill_dcm.generate_personal_name()
        splitted_pn = pn.split('^')
        self.assertEqual(len(splitted_pn), 2)
        self.assertGreater(len(splitted_pn[0]), 0)
        self.assertGreater(len(splitted_pn[1]), 0)

    def test_generate_date(self):
        """ Test generate_date() 
        """
        date = fill_dcm.generate_date()
        self.assertEqual(len(date), 8)
        self.assertTrue(date.isdigit())
        # Check years
        self.assertLessEqual(int(date[0:4]), 2020)
        # Check months
        self.assertLessEqual(int(date[4:6]), 12)
        # Check days
        self.assertLessEqual(int(date[6:]), 31)

    def test_generate_patient_id(self):
        """ Test generate_patient_id()
        """
        patient_id = fill_dcm.generate_id()
        self.assertGreater(len(patient_id), 0)

    def test_generate_lo(self):
        """ Test generate_lo() 
        """
        long_string = fill_dcm.generate_lo()
        self.assertLessEqual(len(long_string), 64)
        self.assertGreaterEqual(len(long_string), 1)

    def test_generate_age_string(self):
        """ Test generate_age_string()
        """
        age_string = fill_dcm.generate_age_string()
        self.assertEqual(len(age_string), 4)
        self.assertTrue(age_string[0:3].isdigit())
        self.assertEqual(age_string[-1], "Y")

    def test_generate_decimal_string(self):
        """ Test generate_decimal_string()
        """
        decimal_string = fill_dcm.generate_decimal_string()
        self.assertNotEqual(len(decimal_string), 0)
        self.assertLessEqual(len(decimal_string), 16)
        for c in list(decimal_string):
            self.assertIn(c, string.digits)

    def test_generate_date_time(self):
        """ Test generate_date_time() 
        """
        date_time = fill_dcm.generate_date_time()
        self.assertEqual(len(date_time), 14)
        self.assertTrue(date_time.isdigit())
        # Check years
        self.assertLessEqual(int(date_time[0:4]), 2020)
        # Check months
        self.assertLessEqual(int(date_time[4:6]), 12)
        # Check days
        self.assertLessEqual(int(date_time[6:8]), 31)
        # Check hours
        self.assertLessEqual(int(date_time[8:10]), 23)
        # Check minutes
        self.assertLessEqual(int(date_time[10:12]), 59)
        # Check seconds
        self.assertLessEqual(int(date_time[12:]), 59)

    def test_generate_integer_string(self):
        """ Test generate_integer_string()
        """
        integer_string = fill_dcm.generate_integer_string()
        integer = int(integer_string)
        self.assertGreaterEqual(integer, -1*2**31)
        self.assertLessEqual(integer, (2**31)-1)

    def test_generate_long_text(self):
        """ Test generate_long_text() 
        """
        long_text = fill_dcm.generate_long_text()
        self.assertLessEqual(len(long_text), 1024)
        self.assertGreaterEqual(len(long_text), 1)

    def test_generate_short_string(self):
        """ Test generate_short_string() 
        """
        short_string = fill_dcm.generate_short_string()
        self.assertLessEqual(len(short_string), 16)
        self.assertGreaterEqual(len(short_string), 1)

    def test_generate_short_text(self):
        """ Test generate_short_text() 
        """
        short_text = fill_dcm.generate_short_text()
        self.assertLessEqual(len(short_text), 1024)
        self.assertGreaterEqual(len(short_text), 1)

    def test_generate_time(self):
        """ Test generate_time() 
        """
        time = fill_dcm.generate_time()
        self.assertEqual(len(time), 6)
        self.assertTrue(time.isdigit())
        # Check hours
        self.assertLessEqual(int(time[0:2]), 23)
        # Check minutes
        self.assertLessEqual(int(time[2:4]), 59)
        # Check seconds
        self.assertLessEqual(int(time[4:]), 59)

    def test_generate_unique_identifier(self):
        """ Test generate_unique_identifier()
        """
        unique_identifier = fill_dcm.generate_unique_identifier()
        self.assertLessEqual(len(unique_identifier), 64)
        splitted_uid = unique_identifier.split('.')
        self.assertEqual(len(splitted_uid), 4)
        for part in splitted_uid:
            int(part)  # each part is a number

    def test_generate_unsigned_short(self):
        """ Test generate_unsigned_short()
        """
        unsigned_short = fill_dcm.generate_unsigned_short()
        self.assertGreaterEqual(unsigned_short, 0)
        self.assertLess(unsigned_short, 65536)
