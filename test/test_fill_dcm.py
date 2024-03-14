import unittest
from filldcm import fill_dcm


class TestFillDCM(unittest.TestCase):
    """ Test methods from fill_dcm
    """

    def test_verify_input_tags_tag_not_empty(self):
        """ fill_dcm.verify_input_tags() shall throw if no tag is defined
        """
        self.assertRaises(fill_dcm.InvalidParameter, fill_dcm.verify_input_tags, {
                          "tags": {}, "tags_to_overwrite": {}})

        fill_dcm.verify_input_tags({"tags": {}, "tags_to_overwrite": {
            "PatientID": "Value"}})  # Shall not throw
        # Shall not throw
        fill_dcm.verify_input_tags(
            {"tags": {"SeriesDate": None}, "tags_to_overwrite": {}})

    def test_verify_input_tags_tag_no_duplicate(self):
        """  fill_dcm.verify_input_tags() shall throw if tags are duplicated between the two lists
        """
        self.assertRaises(fill_dcm.InvalidParameter, fill_dcm.verify_input_tags, {
                          "tags": {"MyTag": None}, "tags_to_overwrite": {"MyTag": "MyValue"}})

        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          {"tags": {"MyTag": None, "MySecondTag": None}, "tags_to_overwrite": {"MyTag": "MyValue", "SimpleTag": "SimpleValue"}})

    def test_verify_input_tags_tag_to_overwrite_have_values(self):
        """ fill_dcm.verify_input_tags() shall throw if a tag to overwrite has no value
        """
        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          {"tags": {}, "tags_to_overwrite": {"PatientName": None}})

        fill_dcm.verify_input_tags(
            {"tags": {"SeriesTime": None}, "tags_to_overwrite": {}})  # shall not throw

    def test_verify_input_tags_valid_dicom_tags(self):
        """ If tag is not in DICOM dictionary an exception is raised
        """
        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          {"tags": {"InvalidTagName": None}, "tags_to_overwrite": {}})
        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          {"tags": {}, "tags_to_overwrite": {"ImaginaryTagName": "NoValue"}})
        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          {"tags": {"PatientId": None, "PatientNotExistTag": None}, "tags_to_overwrite": {}})
        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          {"tags": {}, "tags_to_overwrite": {"PatientId": None, "PatientNotExistTag": None}})

    def test_verify_input_tags_valid(self):
        """ fill_dcm.verify_input_tags() shall not throw with valid inputs
        """
        fill_dcm.verify_input_tags(
            {"tags": {"PixelSpacing": None, "PatientName": "Raymond"}, "tags_to_overwrite": {}})
        fill_dcm.verify_input_tags(
            {"tags": {}, "tags_to_overwrite": {"PatientID": "42", "PatientName": "Raymond"}})
