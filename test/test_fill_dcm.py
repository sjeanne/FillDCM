import unittest

from filldcm import parse_argument


class TestFillDCM(unittest.TestCase):
    """Test methods from parse_argument"""

    def test_verify_input_tags_tag_not_empty(self):
        """parse_argument.verify_input_tags() shall throw if no tag is defined"""
        self.assertRaises(
            parse_argument.InvalidArgument,
            parse_argument.verify_input_tags,
            parse_argument.InputTags(),
        )

        # Shall not throw
        parse_argument.verify_input_tags(
            parse_argument.InputTags({}, {"PatientID": "Value"})
        )

        # Shall not throw
        parse_argument.verify_input_tags(
            parse_argument.InputTags({"SeriesDate": None}, {})
        )

    def test_verify_input_tags_tag_no_duplicate(self):
        """parse_argument.verify_input_tags() shall throw if tags are duplicated between the two lists"""
        self.assertRaises(
            parse_argument.InvalidArgument,
            parse_argument.verify_input_tags,
            parse_argument.InputTags({"MyTag": None}, {"MyTag": "MyValue"}),
        )

        self.assertRaises(
            parse_argument.InvalidArgument,
            parse_argument.verify_input_tags,
            parse_argument.InputTags(
                {"MyTag": None, "MySecondTag": None},
                {"MyTag": "MyValue", "SimpleTag": "SimpleValue"},
            ),
        )

    def test_verify_input_tags_tag_to_overwrite_have_values(self):
        """parse_argument.verify_input_tags() shall throw if a tag to overwrite has no value"""
        self.assertRaises(
            parse_argument.InvalidArgument,
            parse_argument.verify_input_tags,
            parse_argument.InputTags({}, {"PatientName": None}),
        )

        # shall not throw
        parse_argument.verify_input_tags(
            parse_argument.InputTags({"SeriesTime": None}, {})
        )

    def test_verify_input_tags_valid_dicom_tags(self):
        """If tag is not in DICOM dictionary an exception is raised"""
        self.assertRaises(
            parse_argument.InvalidArgument,
            parse_argument.verify_input_tags,
            parse_argument.InputTags({"InvalidTagName": None}, {}),
        )
        self.assertRaises(
            parse_argument.InvalidArgument,
            parse_argument.verify_input_tags,
            parse_argument.InputTags({}, {"ImaginaryTagName": "NoValue"}),
        )
        self.assertRaises(
            parse_argument.InvalidArgument,
            parse_argument.verify_input_tags,
            parse_argument.InputTags(
                {"PatientId": None, "PatientNotExistTag": None}, {}
            ),
        )
        self.assertRaises(
            parse_argument.InvalidArgument,
            parse_argument.verify_input_tags,
            parse_argument.InputTags(
                {}, {"PatientId": None, "PatientNotExistTag": None}
            ),
        )

    def test_verify_input_tags_valid(self):
        """parse_argument.verify_input_tags() shall not throw with valid inputs"""
        parse_argument.verify_input_tags(
            parse_argument.InputTags(
                {"PixelSpacing": None, "PatientName": "Raymond"}, {}
            )
        )
        parse_argument.verify_input_tags(
            parse_argument.InputTags({}, {"PatientID": "42", "PatientName": "Raymond"})
        )
