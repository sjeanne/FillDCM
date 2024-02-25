import unittest
from fill_dcm import verify_input_tags, InvalidParameter


class TestFillDCM(unittest.TestCase):
    """ Test methods from fill_dcm
    """

    def test_verify_input_tags_tag_not_empty(self):
        """ verify_input_tags() shall throw if no tag is defined
        """
        self.assertRaises(InvalidParameter, verify_input_tags, {
                          "tags": {}, "tags_to_overwrite": {}})

        verify_input_tags({"tags": {}, "tags_to_overwrite": {
                          "PatientID": "Value"}})  # Shall not throw
        # Shall not throw
        verify_input_tags(
            {"tags": {"SeriesDate": None}, "tags_to_overwrite": {}})

    def test_verify_input_tags_tag_no_duplicate(self):
        """  verify_input_tags() shall throw if tags are duplicated between the two lists
        """
        self.assertRaises(InvalidParameter, verify_input_tags, {
                          "tags": {"MyTag": None}, "tags_to_overwrite": {"MyTag": "MyValue"}})

        self.assertRaises(InvalidParameter,
                          verify_input_tags,
                          {"tags": {"MyTag": None, "MySecondTag": None}, "tags_to_overwrite": {"MyTag": "MyValue", "SimpleTag": "SimpleValue"}})

    def test_verify_input_tags_tag_to_overwrite_have_values(self):
        """ verify_input_tags() shall throw if a tag to overwrite has no value
        """
        self.assertRaises(InvalidParameter,
                          verify_input_tags,
                          {"tags": {}, "tags_to_overwrite": {"PatientName": None}})

        verify_input_tags(
            {"tags": {"SeriesTime": None}, "tags_to_overwrite": {}})  # shall not throw

    def test_verify_input_tags_valid_dicom_tags(self):
        """ If tag is not in DICOM dictionary an exception is raised
        """
        self.assertRaises(InvalidParameter,
                          verify_input_tags,
                          {"tags": {"InvalidTagName": None}, "tags_to_overwrite": {}})
        self.assertRaises(InvalidParameter,
                          verify_input_tags,
                          {"tags": {}, "tags_to_overwrite": {"ImaginaryTagName": "NoValue"}})
        self.assertRaises(InvalidParameter,
                          verify_input_tags,
                          {"tags": {"PatientId": None, "PatientNotExistTag": None}, "tags_to_overwrite": {}})
        self.assertRaises(InvalidParameter,
                          verify_input_tags,
                          {"tags": {}, "tags_to_overwrite": {"PatientId": None, "PatientNotExistTag": None}})

    def test_verify_input_tags_valid(self):
        """ verify_input_tags() shall not throw with valid inputs
        """
        verify_input_tags(
            {"tags": {"PixelSpacing": None, "PatientName": "Raymond"}, "tags_to_overwrite": {}})
        verify_input_tags(
            {"tags": {}, "tags_to_overwrite": {"PatientID": "42", "PatientName": "Raymond"}})
