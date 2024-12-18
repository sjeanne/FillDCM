import argparse
from typing import Dict, List, Tuple

from pydicom import datadict


class InvalidArgument(Exception):
    """Exception to handle CLI parameter errors"""


class InputTags:
    """Contains all DICOM tags to fill or to replace"""

    def __init__(
        self,
        tags_to_fill: Dict[str, str] = None,
        tags_to_replace: Dict[str, str] = None,
    ):
        """InputTags constructor

        Args:
            tags_to_fill (dict, optional): Dictionary of tag to fill. Defaults to None.
            tags_to_replace (dict, optional): Dictionary of tag to replace. Defaults to None.
        """
        self.tags_to_fill: Dict[str, str] = (
            tags_to_fill if tags_to_fill is not None else {}
        )
        self.tags_to_replace: Dict[str, str] = (
            tags_to_replace if tags_to_replace is not None else {}
        )


class Options:
    """Contains application options"""

    def __init__(self, overwrite_output_file: bool = False):
        """Options constructor
        Args:
            overwrite_output_file (bool, optional): Set to True to overwrite DICOM input files. Defaults to False.
        """
        self.overwrite_output_file: bool = overwrite_output_file


def tag_is_in_dicom_dictionary(tag: str) -> bool:
    """Indicated if a tag, by its string value, exist in the DICOM dictionary

    Args:
        tag (str): Tag name to verify

    Returns:
        bool: True if tag exists, otherwise False
    """
    return datadict.dictionary_has_tag(tag)


def verify_input_tags(input_args: InputTags) -> None:
    """Verify validity of inputs arguments. Rules:
        - a tag can't be in both list (tag and tag to replace)
        - a tag to replace must have a value (e.g "tag=value")
        - at least one tag shall be provided
        - tags of both lists must be a valid tag from DICOM dictionary
    Exceptions:
        InvalidArgument if a condition is not matched
    """
    # At least one tag shall be defined
    if (
        len(input_args.tags_to_fill.keys()) == 0
        and len(input_args.tags_to_replace.keys()) == 0
    ):
        raise InvalidArgument("At least one tag shall be defined")

    # Duplication between the two lists of tags
    # and Tags to replace must have a value
    # and Tags to replace shall be in DICOM dictionary
    for tag_to_replace in input_args.tags_to_replace:
        if input_args.tags_to_replace[tag_to_replace] is None:
            raise InvalidArgument(f"Tag {tag_to_replace} must have value.")
        if tag_to_replace in input_args.tags_to_fill:
            raise InvalidArgument(
                f"Tag {tag_to_replace} is duplicated. A tag can only be defined once"
            )
        if not tag_is_in_dicom_dictionary(tag_to_replace):
            raise InvalidArgument(
                f"Tag {tag_to_replace} is not a valid tag from DICOM dictionary"
            )

    # tags shall be in DICOM dictionary
    for tag in input_args.tags_to_fill:
        if not tag_is_in_dicom_dictionary(tag):
            raise InvalidArgument(f"Tag {tag} is not a valid tag from DICOM dictionary")

    # TODO verify that values passed are correct according to  tag's VR.
    # Add an option to enable/disable this check


# TODO add unit test of parse_arguments()
def parse(input_args: argparse.Namespace) -> Tuple[InputTags, Options]:
    """Parse input arguments and return two dictionaries of tag to fill and tag_to_replace and also options

    Args:
        input_args (argparse.Namespace): CLI parameters
    Returns:
        Tuple[InputTags, Options]: InputTags and options parsed from CLI parameters
    """
    parsed_tags = InputTags()

    # tags to fill
    if "fill" in input_args and input_args.fill is not None:
        for raw_tag in input_args.fill:
            splitted_tag = raw_tag.split("=", 1)
            parsed_tags.tags_to_fill[splitted_tag[0]] = (
                None if len(splitted_tag) == 1 else splitted_tag[1]
            )

    # tags to replace
    if "replace" in input_args and input_args.replace is not None:
        for raw_tag_to_replace in input_args.replace:
            splitted_tag = raw_tag_to_replace.split("=", 1)
            parsed_tags.tags_to_replace[splitted_tag[0]] = (
                None if len(splitted_tag) == 1 else splitted_tag[1]
            )

    # TODO: excluse JSON with regular inputs
    if "json_path" in input_args and input_args.json_path is not None:
        try:
            with open(input_args.json_path, "r") as json_file:
                parsed_json = json.load(json_file)
                parsed_tags = InputTags(
                    parsed_json.get("tags_to_fill", None),
                    parsed_json.get("tags_to_replace", None),
                )
        except Exception as error:
            raise InvalidArgument(
                f"Error while reading JSON input. File: {input_args.json_path}. Error:{error}"
            )

    options = Options(input_args.overwrite_file)

    return (parsed_tags, options)
