""" Test fill_dcm.update_data() unit tests
"""

import unittest
from copy import deepcopy

from fill_dcm import fill_dcm, parse_argument


class TestDataUpdate(unittest.TestCase):
    """Test fill_dcm.update_data()"""

    def test_update_data_values(self):
        """Call to update_data() with input values. Only 'None' tags are updated with  a random value"""
        input_values = parse_argument.InputTags(
            {
                "PatientName": "patient^name^complicated",
                "PatientID": "1234567890AZERTY",
                "PatientBirthDate": "20000101",
                "ReferringPhysicianName": None,
                "DeviceSerialNumber": None,
            },
            {},
        )

        updated_values = deepcopy(input_values)
        fill_dcm.update_data(updated_values)

        # Tags are not updated
        self.assertEqual(
            updated_values.tags_to_fill["PatientName"],
            input_values.tags_to_fill["PatientName"],
        )
        self.assertEqual(
            updated_values.tags_to_fill["PatientID"],
            input_values.tags_to_fill["PatientID"],
        )
        self.assertEqual(
            updated_values.tags_to_fill["PatientBirthDate"],
            input_values.tags_to_fill["PatientBirthDate"],
        )
        # Tags have a value defined now
        self.assertIsNotNone(updated_values.tags_to_fill["ReferringPhysicianName"])
        self.assertIsNotNone(updated_values.tags_to_fill["DeviceSerialNumber"])

    def test_tags_to_overwrite_not_updated(self):
        """Tags to overwrite are not updated"""
        input_values = parse_argument.InputTags(
            {},
            {
                "PatientID": "1234567890AZERTY",
                "PatientName": "patient^name^complicated",
            },
        )

        updated_values = deepcopy(input_values)
        fill_dcm.update_data(updated_values)

        # Tags shall not be updated
        self.assertEqual(
            input_values.tags_to_replace["PatientID"],
            updated_values.tags_to_replace["PatientID"],
        )
        self.assertEqual(
            input_values.tags_to_replace["PatientName"],
            updated_values.tags_to_replace["PatientName"],
        )

    def test_update_data_with_empty_input(self):
        """Empty structure is passed, no exception are raised."""
        fill_dcm.update_data(parse_argument.InputTags())

    def test_update_data_vr_as(self):
        """AS VR is managed, update_data() creates a value for AG tags"""
        input_values = parse_argument.InputTags({"PatientAge": None}, {})
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values.tags_to_fill["PatientAge"])

    def test_update_data_vr_ds(self):
        """DS VR is managed, update_data() creates a value for DS tags"""
        input_values = parse_argument.InputTags({"PixelSpacing": None}, {})
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values.tags_to_fill["PixelSpacing"])

    def test_update_data_vr_dt(self):
        """DT VR is managed, update_data() creates a value for DT tags"""
        input_values = parse_argument.InputTags({"AcquisitionDateTime": None}, {})
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values.tags_to_fill["AcquisitionDateTime"])

    def test_update_data_vr_is(self):
        """IS VR is managed, update_data() creates a value for IS tags"""
        input_values = parse_argument.InputTags({"SeriesNumber": None}, {})
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values.tags_to_fill["SeriesNumber"])

    def test_update_data_vr_lt(self):
        """LT VR is managed, update_data() creates a value for LT tags"""
        input_values = parse_argument.InputTags({"ImageComments": None}, {})
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values.tags_to_fill["ImageComments"])

    def test_update_data_vr_sh(self):
        """SH VR is managed, update_data() creates a value for SH tags"""
        input_values = parse_argument.InputTags({"StationName": None}, {})
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values.tags_to_fill["StationName"])

    def test_update_data_vr_st(self):
        """ST VR is managed, update_data() creates a value for ST tags"""
        input_values = parse_argument.InputTags({"InstitutionAddress": None}, {})
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values.tags_to_fill["InstitutionAddress"])

    def test_update_data_throw_vr_tm(self):
        """TM VR is managed, update_data() creates a value for TM tags"""
        input_values = parse_argument.InputTags({"SeriesTime": None}, {})
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values.tags_to_fill["SeriesTime"])

    def test_update_data_throw_vr_ui(self):
        """UI VR is managed, update_data() creates a value for UI tags"""
        input_values = parse_argument.InputTags({"DeviceUID": None}, {})
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values.tags_to_fill["DeviceUID"])

    def test_update_data_throw_vr_us(self):
        """US VR is managed, update_data() creates a value for US tags"""
        input_values = parse_argument.InputTags({"Rows": None}, {})
        fill_dcm.update_data(input_values)
        self.assertIsNotNone(input_values.tags_to_fill["Rows"])
