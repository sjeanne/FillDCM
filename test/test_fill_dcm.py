import unittest
from filldcm import fill_dcm


class TestFillDCM(unittest.TestCase):
    """ Test methods from fill_dcm
    """

    def test_verify_input_tags_tag_not_empty(self):
        """ fill_dcm.verify_input_tags() shall throw if no tag is defined
        """
        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags, fill_dcm.InputTags())

        # Shall not throw
        fill_dcm.verify_input_tags(
            fill_dcm.InputTags({}, {"PatientID": "Value"}))

        # Shall not throw
        fill_dcm.verify_input_tags(
            fill_dcm.InputTags({"SeriesDate": None}, {}))

    def test_verify_input_tags_tag_no_duplicate(self):
        """  fill_dcm.verify_input_tags() shall throw if tags are duplicated between the two lists
        """
        self.assertRaises(fill_dcm.InvalidParameter, fill_dcm.verify_input_tags,
                          fill_dcm.InputTags({"MyTag": None}, {"MyTag": "MyValue"}))

        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          fill_dcm.InputTags({"MyTag": None, "MySecondTag": None}, {"MyTag": "MyValue", "SimpleTag": "SimpleValue"}))

    def test_verify_input_tags_tag_to_overwrite_have_values(self):
        """ fill_dcm.verify_input_tags() shall throw if a tag to overwrite has no value
        """
        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          fill_dcm.InputTags({}, {"PatientName": None}))

        # shall not throw
        fill_dcm.verify_input_tags(
            fill_dcm.InputTags({"SeriesTime": None}, {}))

    def test_verify_input_tags_valid_dicom_tags(self):
        """ If tag is not in DICOM dictionary an exception is raised
        """
        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          fill_dcm.InputTags({"InvalidTagName": None}, {}))
        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          fill_dcm.InputTags({}, {"ImaginaryTagName": "NoValue"}))
        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          fill_dcm.InputTags({"PatientId": None, "PatientNotExistTag": None}, {}))
        self.assertRaises(fill_dcm.InvalidParameter,
                          fill_dcm.verify_input_tags,
                          fill_dcm.InputTags({}, {"PatientId": None, "PatientNotExistTag": None}))

    def test_verify_input_tags_valid(self):
        """ fill_dcm.verify_input_tags() shall not throw with valid inputs
        """
        fill_dcm.verify_input_tags(
            fill_dcm.InputTags({"PixelSpacing": None, "PatientName": "Raymond"}, {}))
        fill_dcm.verify_input_tags(
            fill_dcm.InputTags({}, {"PatientID": "42", "PatientName": "Raymond"}))
