import unittest
from unittest.mock import Mock, mock_open, patch

from fill_dcm import parse_argument


class TestParseArgument(unittest.TestCase):
    """Test methods from parse_argument"""

    def test_verify_input_tags_tag_not_empty(self):
        """parse_argument.verify_input_tags() shall throw if no tag is defined"""
        self.assertRaises(
            parse_argument.InvalidArgument,
            parse_argument.verify_input_tags,
            parse_argument.InputTags(),
        )

        # Shall not throw
        parse_argument.verify_input_tags(parse_argument.InputTags({}, {"PatientID": "Value"}))

        # Shall not throw
        parse_argument.verify_input_tags(parse_argument.InputTags({"SeriesDate": None}, {}))

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
        parse_argument.verify_input_tags(parse_argument.InputTags({"SeriesTime": None}, {}))

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
            parse_argument.InputTags({"PatientId": None, "PatientNotExistTag": None}, {}),
        )
        self.assertRaises(
            parse_argument.InvalidArgument,
            parse_argument.verify_input_tags,
            parse_argument.InputTags({}, {"PatientId": None, "PatientNotExistTag": None}),
        )

    def test_verify_input_tags_valid(self):
        """parse_argument.verify_input_tags() shall not throw with valid inputs"""
        parse_argument.verify_input_tags(parse_argument.InputTags({"PixelSpacing": None, "PatientName": "Raymond"}, {}))
        parse_argument.verify_input_tags(parse_argument.InputTags({}, {"PatientID": "42", "PatientName": "Raymond"}))

    def test_parse_with_tag_to_fill_one_tag_with_value(self):
        """parse_argument.parse() shall parse tag to fill: one tag with value"""
        tag_value1 = ("PatientName", "Wayne^Bruce")
        args = Mock(fill=[f"{tag_value1[0]}={tag_value1[1]}"], replace=None, json_path=None)
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(input_tags.tags_to_fill[tag_value1[0]], tag_value1[1])
        self.assertEqual(len(input_tags.tags_to_replace), 0)

    def test_parse_with_tag_to_fill_tags_with_values(self):
        """parse_argument.parse() shall parse tag to fill: several tags with value"""
        tag_value1 = ("PatientName", "Wayne^Bruce")
        tag_value2 = ("PatientAge", "O40Y")
        tag_value3 = ("AcquisitionDate", "20241225")
        args = Mock(
            fill=[
                f"{tag_value1[0]}={tag_value1[1]}",
                f"{tag_value2[0]}={tag_value2[1]}",
                f"{tag_value3[0]}={tag_value3[1]}",
            ],
            replace=None,
            json_path=None,
        )
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(input_tags.tags_to_fill[tag_value1[0]], tag_value1[1])
        self.assertEqual(input_tags.tags_to_fill[tag_value2[0]], tag_value2[1])
        self.assertEqual(input_tags.tags_to_fill[tag_value3[0]], tag_value3[1])
        self.assertEqual(len(input_tags.tags_to_replace), 0)

    def test_parse_with_tag_to_fill_one_tag(self):
        """parse_argument.parse() shall parse tag to fill: one tag without value"""
        tag1 = "PatientID"
        args = Mock(fill=[f"{tag1}"], replace=None, json_path=None)
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(input_tags.tags_to_fill[tag1], None)
        self.assertEqual(len(input_tags.tags_to_replace), 0)

    def test_parse_with_tag_to_fill_tags(self):
        """parse_argument.parse() shall parse tag to fill: tags without value"""
        tag1 = "PatientID"
        tag2 = "PatientSex"
        tag3 = "SeriesTime"
        args = Mock(fill=[f"{tag1}", f"{tag2}", f"{tag3}"], replace=None, json_path=None)
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(input_tags.tags_to_fill[tag1], None)
        self.assertEqual(input_tags.tags_to_fill[tag2], None)
        self.assertEqual(input_tags.tags_to_fill[tag3], None)
        self.assertEqual(len(input_tags.tags_to_replace), 0)

    def test_parse_with_tag_to_replace_one_tag(self):
        """parse_argument.parse() shall parse tag to replace: one tag"""
        tag1 = ("SeriesDate", "20241225")
        args = Mock(fill=None, replace=[f"{tag1[0]}={tag1[1]}"], json_path=None)
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(input_tags.tags_to_replace[tag1[0]], tag1[1])
        self.assertEqual(len(input_tags.tags_to_fill), 0)

    def test_parse_with_tag_to_replace_tags(self):
        """parse_argument.parse() shall parse tag to replace: several tags"""
        tag_value1 = ("PatientName", "Wayne^Bruce")
        tag_value2 = ("PatientAge", "O40Y")
        tag_value3 = ("AcquisitionDate", "20241225")
        args = Mock(
            fill=None,
            replace=[
                f"{tag_value1[0]}={tag_value1[1]}",
                f"{tag_value2[0]}={tag_value2[1]}",
                f"{tag_value3[0]}={tag_value3[1]}",
            ],
            json_path=None,
        )
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(input_tags.tags_to_replace[tag_value1[0]], tag_value1[1])
        self.assertEqual(input_tags.tags_to_replace[tag_value2[0]], tag_value2[1])
        self.assertEqual(input_tags.tags_to_replace[tag_value3[0]], tag_value3[1])
        self.assertEqual(len(input_tags.tags_to_fill), 0)

    def test_parse_with_tag_to_replace_tags(self):
        """parse_argument.parse() shall parse tag to replace: several tags"""
        tag_value1 = ("PatientName", "Wayne^Bruce")
        tag_value2 = ("PatientAge", "O40Y")
        tag_value3 = ("AcquisitionDate", "20241225")
        args = Mock(
            fill=None,
            replace=[
                f"{tag_value1[0]}={tag_value1[1]}",
                f"{tag_value2[0]}={tag_value2[1]}",
                f"{tag_value3[0]}={tag_value3[1]}",
            ],
            json_path=None,
        )
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(input_tags.tags_to_replace[tag_value1[0]], tag_value1[1])
        self.assertEqual(input_tags.tags_to_replace[tag_value2[0]], tag_value2[1])
        self.assertEqual(input_tags.tags_to_replace[tag_value3[0]], tag_value3[1])
        self.assertEqual(len(input_tags.tags_to_fill), 0)

    def test_parse_with_tags_to_fill_and_replace(self):
        """parse_argument.parse() shall parse tags to fill and to replace"""
        tag_value1 = "PatientName"
        tag_value2 = ("PatientAge", "O40Y")
        tag_value3 = ("AcquisitionDate", "20241225")
        tag_value4 = ("AcquisitionTime", "123456")
        args = Mock(
            fill=[f"{tag_value1}", f"{tag_value2[0]}={tag_value2[1]}"],
            replace=[
                f"{tag_value3[0]}={tag_value3[1]}",
                f"{tag_value4[0]}={tag_value4[1]}",
            ],
            json_path=None,
        )
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(input_tags.tags_to_fill[tag_value1], None)
        self.assertEqual(input_tags.tags_to_fill[tag_value2[0]], tag_value2[1])
        self.assertEqual(input_tags.tags_to_replace[tag_value3[0]], tag_value3[1])
        self.assertEqual(input_tags.tags_to_replace[tag_value4[0]], tag_value4[1])

    def test_parse_without_tag(self):
        """parse_argument.parse() shall not fail if no tag is passed"""
        args = Mock(fill=None, replace=None, json_path=None)
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(len(input_tags.tags_to_fill), 0)
        self.assertEqual(len(input_tags.tags_to_replace), 0)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"tags_to_fill":{"PatientName":"Wayne^Bruce", "PatientID":null}, "tags_to_replace":{"AcquisitionDate":"20241225"} }',
    )
    def test_parse_json_tag(self, mocked_open):
        """parse_argument.parse() shall read json input"""
        args = Mock(fill=None, replace=None, json_path="/foo/bar.json")
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(len(input_tags.tags_to_fill), 2)
        self.assertEqual(input_tags.tags_to_fill["PatientName"], "Wayne^Bruce")
        self.assertIsNone(input_tags.tags_to_fill["PatientID"])
        self.assertEqual(len(input_tags.tags_to_replace), 1)
        self.assertEqual(input_tags.tags_to_replace["AcquisitionDate"], "20241225")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="{}",
    )
    def test_parse_empty_json_file(self, mocked_open):
        """parse_argument.parse() shall read an empty json file"""
        args = Mock(fill=None, replace=None, json_path="/foo/bar.json")
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(len(input_tags.tags_to_fill), 0)
        self.assertEqual(len(input_tags.tags_to_replace), 0)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"non_expected_tag":42, "FillDCM":{"copyright":2024}}',
    )
    def test_parse_unexpected_json_file(self, mocked_open):
        """parse_argument.parse() shall read a json file with unexpected tags"""
        args = Mock(fill=None, replace=None, json_path="/foo/bar.json")
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(len(input_tags.tags_to_fill), 0)
        self.assertEqual(len(input_tags.tags_to_replace), 0)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="I am not a JSON file.",
    )
    def test_parse_invalid_json_exception(self, mocked_open):
        """parse_argument.parse() shall throw if input file is not a valid JSON"""
        args = Mock(fill=None, replace=None, json_path="/foo/bar.json")
        self.assertRaises(
            parse_argument.InvalidArgument,
            parse_argument.parse,
            args,
        )

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"tags_to_fill":{"PatientName":"Wayne^Bruce", "PatientID":null}, "tags_to_replace":{"AcquisitionDate":"20241225"} }',
    )
    def test_parse_json_and_tags(self, mocked_open):
        """parse_argument.parse() shall json and tags input"""
        args = Mock(
            fill=["PatientName=Tintin", "PatientSex=F"],
            replace=["SeriesDate=20250101"],
            json_path="/foo/bar.json",
        )
        (input_tags, _) = parse_argument.parse(args)
        self.assertEqual(len(input_tags.tags_to_fill), 3)
        self.assertEqual(input_tags.tags_to_fill["PatientName"], "Tintin")
        self.assertEqual(input_tags.tags_to_fill["PatientSex"], "F")
        self.assertIsNone(input_tags.tags_to_fill["PatientID"])
        self.assertEqual(len(input_tags.tags_to_replace), 2)
        self.assertEqual(input_tags.tags_to_replace["AcquisitionDate"], "20241225")
        self.assertEqual(input_tags.tags_to_replace["SeriesDate"], "20250101")

    def test_parse_option_overwrite_true(self):
        """parse_argument.parse() shall parse overwrite option if True"""
        args = Mock(fill=None, replace=None, json_path=None, overwrite_file=True)
        (_, options) = parse_argument.parse(args)
        self.assertTrue(options.overwrite_output_file)

    def test_parse_option_overwrite_false(self):
        """parse_argument.parse() shall parse overwrite option if False"""
        args = Mock(fill=None, replace=None, json_path=None, overwrite_file=False)
        (_, options) = parse_argument.parse(args)
        self.assertFalse(options.overwrite_output_file)

    def test_parse_option_overwrite_none(self):
        """parse_argument.parse() shall parse overwrite option if None"""
        args = Mock(fill=None, replace=None, json_path=None, overwrite_file=None)
        (_, options) = parse_argument.parse(args)
        self.assertFalse(options.overwrite_output_file)

    def test_parse_option_verbose_true(self):
        """parse_argument.parse() shall parse verbose option if True"""
        args = Mock(fill=None, replace=None, json_path=None, verbose_log=True)
        (_, options) = parse_argument.parse(args)
        self.assertTrue(options.verbose_log)

    def test_parse_option_verbose_false(self):
        """parse_argument.parse() shall parse verbose option if False"""
        args = Mock(fill=None, replace=None, json_path=None, verbose_log=False)
        (_, options) = parse_argument.parse(args)
        self.assertFalse(options.verbose_log)

    def test_parse_option_verbose_none(self):
        """parse_argument.parse() shall parse verbose option if None"""
        args = Mock(fill=None, replace=None, json_path=None, verbose_log=None)
        (_, options) = parse_argument.parse(args)
        self.assertFalse(options.verbose_log)

    def test_parse_option_verbose_and_overwrite_true(self):
        """parse_argument.parse() shall parse verbose and overwrite option if True"""
        args = Mock(
            fill=None,
            replace=None,
            json_path=None,
            verbose_log=True,
            overwrite_file=True,
        )
        (_, options) = parse_argument.parse(args)
        self.assertTrue(options.verbose_log)
        self.assertTrue(options.overwrite_output_file)
