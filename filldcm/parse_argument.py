from argparse import Namespace
from json import load as json_load
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

    def __init__(self, overwrite_output_file: bool = False, verbose_log: bool = False):
        """Options constructor
        Args:
            overwrite_output_file (bool, optional): Set to True to overwrite DICOM input files. Defaults to False.
            verbose_log (bool, optional): Set to True to enable verbose mode. Defaults to False.
        """
        self.overwrite_output_file: bool = overwrite_output_file
        self.verbose_log: bool = verbose_log


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


def parse(input_args: Namespace) -> Tuple[InputTags, Options]:
    """Parse input arguments and return a tuple of InputTags filled according to input parameters and Options.
        InputTags is filled according to parameter.
        For the JSON option, this structure is expected: { "tags_to_fill": {}, "tags_to_replace":{}} with both attributes being dict.
        If a DICOM tag is passed in the JSON and in the --fill or --replace parameter, the latest override the tag.

    Args:
        input_args (argparse.Namespace): CLI parameters
    Returns:
        Tuple[InputTags, Options]: InputTags and options parsed from CLI parameters
    """
    input_tags = InputTags()

    # tags from JSON
    if input_args.json_path is not None:
        try:
            with open(input_args.json_path, "r") as json_file:
                parsed_json = json_load(json_file)
                if "tags_to_fill" in parsed_json:
                    input_tags.tags_to_fill.update(parsed_json["tags_to_fill"])
                if "tags_to_replace" in parsed_json:
                    input_tags.tags_to_replace.update(parsed_json["tags_to_replace"])
        except Exception as error:
            raise InvalidArgument(
                f"Error while reading JSON input. File: {input_args.json_path}. Error:{error}"
            )

    # tags to fill
    if input_args.fill is not None:
        for raw_tag in input_args.fill:
            splitted_tag = raw_tag.split("=", 1)
            input_tags.tags_to_fill[splitted_tag[0]] = (
                None if len(splitted_tag) == 1 else splitted_tag[1]
            )

    # tags to replace
    if input_args.replace is not None:
        for raw_tag_to_replace in input_args.replace:
            splitted_tag = raw_tag_to_replace.split("=", 1)
            input_tags.tags_to_replace[splitted_tag[0]] = (
                None if len(splitted_tag) == 1 else splitted_tag[1]
            )

    options = Options(input_args.overwrite_file, input_args.verbose_log)

    return (input_tags, options)
