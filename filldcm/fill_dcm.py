""" fill_dcm
"""

import argparse
from typing import Dict, List, Tuple
from pathlib import Path
from pydicom import dcmread, datadict, errors
from filldcm import vr_generators


class InvalidParameter(Exception):
    """ Exception to handle CLI parameter errors
    """


class InputTags():
    """ Contains all DICOM tags to fill or to overwrite
    """

    def __init__(self, tags: Dict[str, str] = None, tags_to_overwrite: Dict[str, str] = None):
        """InputTags constructor

        Args:
            tags (dict, optional): Dictionary of tag to fill. Defaults to None.
            tags_to_overwrite (dict, optional): Dictionary of tag to overwrite. Defaults to None.
        """
        if tags is None:
            tags = {}
        if tags_to_overwrite is None:
            tags_to_overwrite = {}
        self.tags: Dict[str, str] = tags
        self.tags_to_overwrite: Dict[str, str] = tags_to_overwrite


class Options():
    """ Contains application options
    """

    def __init__(self, overwrite_output_file: bool = False):
        """ Options constructor
        Args:
            overwrite_output_file (bool, optional): Set to True to overwrite DICOM input files. Defaults to False.
        """
        self.overwrite_output_file: bool = overwrite_output_file


def update_data(input_values: InputTags) -> InputTags:
    """ Define a value to each tag without. The generated value matches tag's VR. 
        If a tag has a defined value, it is not updated.
        Parameters:
            input_values : InputTags Values defined by the caller
    """
    for tag in input_values.tags:
        if input_values.tags[tag] is None:
            tag_vr = datadict.dictionary_VR(tag)
            tag_generator = None
            match(tag_vr):
                case 'AS':
                    tag_generator = vr_generators.generate_age_string
                case 'DA':
                    tag_generator = vr_generators.generate_date
                case 'DS':
                    tag_generator = vr_generators.generate_decimal_string
                case 'DT':
                    tag_generator = vr_generators.generate_date_time
                case 'IS':
                    tag_generator = vr_generators.generate_integer_string
                case 'LO':
                    tag_generator = vr_generators.generate_lo
                case 'LT':
                    tag_generator = vr_generators.generate_long_text
                case 'PN':
                    tag_generator = vr_generators.generate_personal_name
                case 'SH':
                    tag_generator = vr_generators.generate_short_string
                case 'ST':
                    tag_generator = vr_generators.generate_short_text
                case 'TM':
                    tag_generator = vr_generators.generate_time
                case 'UI':
                    tag_generator = vr_generators.generate_unique_identifier
                case 'US':
                    tag_generator = vr_generators.generate_unsigned_short
                case _:
                    raise InvalidParameter(
                        f"VR: {tag_vr} for tag {tag} not managed")
            input_values.tags[tag] = tag_generator()
    return input_values


def adjust_dicom_dataset(dataset, input_tags: InputTags):
    """ Replace in the dataset empty or missing tags by replacement data
        Parameters:
            dataset (Dataset) Dataset to adjust
            input_tags (InputTags) Data used to replace or overwrite DICOM tags
    """
    # Replace only empty/missing  DICOM tags
    for dcm_tag, tag_value in input_tags.tags.items():
        if not dcm_tag in dataset:
            dataset.add_new(dcm_tag, datadict.dictionary_VR(
                dcm_tag), tag_value)
        elif dataset[dcm_tag].VM == 0:
            dataset[dcm_tag].value = tag_value

    # Overwrite or insert all specified tags
    for dcm_tag, tag_value in input_tags.tags_to_overwrite.items():
        if not dcm_tag in dataset:
            dataset.add_new(dcm_tag, datadict.dictionary_VR(
                dcm_tag), tag_value)
        else:
            dataset[dcm_tag].value = tag_value


def output_filepath(original_file_path: str, overwrite_output_file: bool = False) -> str:
    """ Generate the output filepath. If no overwrite, '_modified' is appended to the input. Otherwise, the input is returned
    Args:
        original_file_path (string) Path to the input file
        overwrite_option (boolean, optional) True to overwrite the input file
    """
    output_file_path = original_file_path
    if not overwrite_output_file:
        path_to_file = Path(original_file_path)
        output_file_path = f"{path_to_file.parent}/{path_to_file.stem}_modified{path_to_file.suffix}"
    return output_file_path


def adjust_dicom_files(files: List[str], input_tags: InputTags, options: Options) -> None:
    """ Adjust DICOM files according to rules and values passed as input

    Args:
        files ([str]): list of path to DICOM files
        input_tags (InputTags): Tags to replace/filled in the list of DICOM files
        options (Options): Options

    """
    update_data(input_tags)

    for file in files:
        print(f"Work on file: {file}")
        try:
            dataset = dcmread(file)
        except errors.InvalidDicomError:
            print(f"Invalid file to read: {file}")
            continue

        adjust_dicom_dataset(dataset, input_tags)
        dataset.save_as(output_filepath(file, options.overwrite_output_file))


def tag_is_in_dicom_dictionary(tag: str) -> bool:
    """ Indicated if a tag, by its string value, exist in the DICOM dictionary

    Args:
        tag (str): Tag name to verify

    Returns:
        bool: True if tag exists, otherwise False
    """
    return datadict.dictionary_has_tag(tag)


def verify_input_tags(input_args: InputTags) -> None:
    """ Verify validity of inputs arguments. Rules:
        - a tag can't be in both list (tag and tag to overwrite)
        - a tag to overwrite must have a value (e.g "tag=value")
        - at least one tag shall be provided
        - tags of both lists must be a valid tag from DICOM dictionary
    Exceptions:
        InvalidParameter if a condition is not matched
    """
    # At least one tag shall be defined
    if len(input_args.tags.keys()) == 0 and len(input_args.tags_to_overwrite.keys()) == 0:
        raise InvalidParameter("At least one tag shall be defined")

    # Duplication between the two lists of tags
    # and Tags to overwrite must have a value
    # and Tags to overwrite shall be in DICOM dictionary
    for tag_to_overwrite in input_args.tags_to_overwrite:
        if input_args.tags_to_overwrite[tag_to_overwrite] is None:
            raise InvalidParameter(
                f"Tag {tag_to_overwrite} must have value.")
        if tag_to_overwrite in input_args.tags:
            raise InvalidParameter(
                f"Tag {tag_to_overwrite} is duplicated. A tag can only be defined once")
        if not tag_is_in_dicom_dictionary(tag_to_overwrite):
            raise InvalidParameter(
                f"Tag {tag_to_overwrite} is not a valid tag from DICOM dictionary")

    # tags shall be in DICOM dictionary
    for tag in input_args.tags:
        if not tag_is_in_dicom_dictionary(tag):
            raise InvalidParameter(
                f"Tag {tag} is not a valid tag from DICOM dictionary")

    # TODO verify that values passed are correct according to  tag's VR.
    # Add an option to enable/disable this check


def parse_arguments(input_args: argparse.Namespace) -> Tuple[InputTags, Options]:
    """ Parse input arguments and return two dictionaries of tag and tag_to_overwrite and also options

    Args:
        input_args (argparse.Namespace): CLI parameters
    Returns:
        Tuple[InputTags, Options]: InputTags and options parsed from CLI parameters
    """
    parsed_tags = InputTags()
    # tags
    if "t" in input_args and input_args.t is not None:
        for raw_tag in input_args.t:
            splitted_tag = raw_tag.split("=", 1)
            parsed_tags.tags[splitted_tag[0]] = None if len(
                splitted_tag) == 1 else splitted_tag[1]

    # tags to overwrite
    if "to" in input_args and input_args.to is not None:
        for raw_tag_to_overwrite in input_args.to:
            splitted_tag = raw_tag_to_overwrite.split("=", 1)
            parsed_tags.tags_to_overwrite[splitted_tag[0]] = None if len(
                splitted_tag) == 1 else splitted_tag[1]

    options = Options(input_args.overwrite_file)

    return (parsed_tags, options)


def fill_dcm_executable() -> None:
    """ Main function that does the job
    """
    command_line = argparse.ArgumentParser(
        prog="FillDCM",
        description="Tool to fill missing or empty DICOM tags or to overwrite others.",
    )
    command_line.add_argument(
        'files', metavar='dcm_file', nargs='+', help="List of DICOM files to edit")
    command_line.add_argument('-t', metavar='--tag', action='append',
                              help="DICOM tag to fill if missing or the value is empty or undefined. Tag specification: <Tag name as a string>[=<value>]")
    command_line.add_argument('-to', metavar='--tag-overwrite', action='append',
                              help="DICOM tag to overwrite with the specified value. Tags specification: <Tag name as a string>=<value>")
    command_line.add_argument(
        '-ov', '--overwrite-file',
        action='store_true',
        help='Overwrite the original file. By default "_generated" is appended the the original filename and a new file is created.')

    # TODO allow to pass tag as tag "0010,0010"

    input_args: argparse.Namespace = command_line.parse_args()

    input_tags, options = parse_arguments(input_args)
    verify_input_tags(input_tags)

    adjust_dicom_files(input_args.files, input_tags, options)


if __name__ == '__main__':
    fill_dcm_executable()
