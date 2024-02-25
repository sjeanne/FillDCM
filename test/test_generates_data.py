""" Data generation functions unit tests
"""

import unittest
from copy import deepcopy
import string
from fill_dcm import generate_personal_name, generate_date, generate_lo, generate_id, update_data, InvalidParameter, generate_age_string, generate_decimal_string, generate_date_time, generate_integer_string, generate_long_text


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
        update_data(updated_values)

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
        update_data(updated_values)

        # Tags shall not be updated
        self.assertEqual(input_values["tags_to_overwrite"]["PatientID"],
                         updated_values["tags_to_overwrite"]["PatientID"])
        self.assertEqual(input_values["tags_to_overwrite"]["PatientName"],
                         updated_values["tags_to_overwrite"]["PatientName"])

    def test_update_data_with_empty_input(self):
        """ Empty structure is passed, no exception are raised.
        """
        update_data({"tags": None, "tags_to_overwrite": None})

    def test_update_data_vr_as(self):
        """ AS VR is managed, update_data() creates a value for AG tags
        """
        input_values = {
            "tags": {"PatientAge": None}, "tags_to_overwrite": None}
        update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["PatientAge"])

    def test_update_data_vr_ds(self):
        """ DS VR is managed, update_data() creates a value for DS tags
        """
        input_values = {
            "tags": {"PixelSpacing": None}, "tags_to_overwrite": None}
        update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["PixelSpacing"])

    def test_update_data_vr_dt(self):
        """ DT VR is managed, update_data() creates a value for DT tags
        """
        input_values = {
            "tags": {"AcquisitionDateTime": None}, "tags_to_overwrite": None}
        update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["AcquisitionDateTime"])

    def test_update_data_vr_is(self):
        """ IS VR is managed, update_data() creates a value for IS tags
        """
        input_values = {
            "tags": {"SeriesNumber": None}, "tags_to_overwrite": None}
        update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["SeriesNumber"])

    def test_update_data_vr_lt(self):
        """ LT VR is managed, update_data() creates a value for LT tags
        """
        input_values = {
            "tags": {"ImageComments": None}, "tags_to_overwrite": None}
        update_data(input_values)
        self.assertIsNotNone(input_values["tags"]["ImageComments"])

    def test_update_data_throw_VR_SH(self):
        """ SH VR is not managed, update_data() raises an InvalidParameter exception
        """
        self.assertRaises(InvalidParameter,
                          update_data, {"tags": {
                              "StationName": None
                          }, "tags_to_overwrite": None})

    def test_update_data_throw_VR_ST(self):
        """ ST VR is not managed, update_data() raises an InvalidParameter exception
        """
        self.assertRaises(InvalidParameter,
                          update_data, {"tags": {
                              "InstitutionAddress": None
                          }, "tags_to_overwrite": None})

    def test_update_data_throw_VR_TM(self):
        """ TM VR is not managed, update_data() raises an InvalidParameter exception
        """
        self.assertRaises(InvalidParameter,
                          update_data, {"tags": {
                              "SeriesTime": None
                          }, "tags_to_overwrite": None})

    def test_update_data_throw_vr_ui(self):
        """ UI VR is not managed, update_data() raises an InvalidParameter exception
        """
        self.assertRaises(InvalidParameter,
                          update_data, {"tags": {
                              "DeviceUID": None
                          }, "tags_to_overwrite": None})

    def test_update_data_throw_vr_us(self):
        """ US VR is not managed, update_data() raises an InvalidParameter exception
        """
        self.assertRaises(InvalidParameter,
                          update_data, {"tags": {
                              "Rows": None
                          }, "tags_to_overwrite": None})

    def test_generate_personal_name(self):
        """ Test generate_personal_name()
        """
        pn = generate_personal_name()
        splitted_pn = pn.split('^')
        self.assertEqual(len(splitted_pn), 2)
        self.assertGreater(len(splitted_pn[0]), 0)
        self.assertGreater(len(splitted_pn[1]), 0)

    def test_generate_date(self):
        """ Test generate_date() 
        """
        date = generate_date()
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
        patient_id = generate_id()
        self.assertGreater(len(patient_id), 0)

    def test_generate_lo(self):
        """ Test generate_lo() 
        """
        long_string = generate_lo()
        self.assertLessEqual(len(long_string), 64)
        self.assertGreaterEqual(len(long_string), 1)

    def test_generate_age_string(self):
        """ Test generate_age_string()
        """
        age_string = generate_age_string()
        self.assertEqual(len(age_string), 4)
        self.assertTrue(age_string[0:3].isdigit())
        self.assertEqual(age_string[-1], "Y")

    def test_generate_decimal_string(self):
        """ Test generate_decimal_string()
        """
        decimal_string = generate_decimal_string()
        self.assertNotEqual(len(decimal_string), 0)
        self.assertLessEqual(len(decimal_string), 16)
        for c in list(decimal_string):
            self.assertIn(c, string.digits)

    def test_generate_date_time(self):
        """ Test generate_date_time() 
        """
        date_time = generate_date_time()
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
        integer_string = generate_integer_string()
        integer = int(integer_string)
        self.assertGreaterEqual(integer, -1*2**31)
        self.assertLessEqual(integer, (2**31)-1)

    def test_generate_long_text(self):
        """ Test generate_long_text() 
        """
        long_text = generate_long_text()
        self.assertLessEqual(len(long_text), 1024)
        self.assertGreaterEqual(len(long_text), 1)
