""" fill_dcm
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple

from pydicom import datadict, dcmread, errors

from filldcm import parse_argument, vr_generators

logger = logging.getLogger()


class InvalidParameter(Exception):
    """Exception to handle CLI parameter errors"""


def update_data(input_values: parse_argument.InputTags) -> parse_argument.InputTags:
    """Define a value to each tag without. The generated value matches tag's VR.
    If a tag has a defined value, it is not updated.
    Parameters:
        input_values : InputTags Values defined by the caller
    """
    for tag in input_values.tags_to_fill:
        if input_values.tags_to_fill[tag] is None:
            tag_vr = datadict.dictionary_VR(tag)
            tag_generator = None
            match (tag_vr):
                case "AS":
                    tag_generator = vr_generators.generate_age_string
                case "DA":
                    tag_generator = vr_generators.generate_date
                case "DS":
                    tag_generator = vr_generators.generate_decimal_string
                case "DT":
                    tag_generator = vr_generators.generate_date_time
                case "IS":
                    tag_generator = vr_generators.generate_integer_string
                case "LO":
                    tag_generator = vr_generators.generate_lo
                case "LT":
                    tag_generator = vr_generators.generate_long_text
                case "PN":
                    tag_generator = vr_generators.generate_personal_name
                case "SH":
                    tag_generator = vr_generators.generate_short_string
                case "ST":
                    tag_generator = vr_generators.generate_short_text
                case "TM":
                    tag_generator = vr_generators.generate_time
                case "UI":
                    tag_generator = vr_generators.generate_unique_identifier
                case "US":
                    tag_generator = vr_generators.generate_unsigned_short
                case _:
                    raise InvalidParameter(f"VR: {tag_vr} for tag {tag} not managed")
            input_values.tags_to_fill[tag] = tag_generator()
    return input_values


def adjust_dicom_dataset(dataset, input_tags: parse_argument.InputTags):
    """Replace in the dataset empty or missing tags by replacement data
    Parameters:
        dataset (Dataset) Dataset to adjust
        input_tags (InputTags) Data used to replace or overwrite DICOM tags
    """
    # Replace only empty/missing  DICOM tags
    for dcm_tag, tag_value in input_tags.tags_to_fill.items():
        if not dcm_tag in dataset:
            dataset.add_new(dcm_tag, datadict.dictionary_VR(dcm_tag), tag_value)
            logger.info(f"Add {dcm_tag}:{tag_value}")
        elif dataset[dcm_tag].VM == 0:
            dataset[dcm_tag].value = tag_value
            logger.info(f"Update {dcm_tag}:{tag_value}")

    # Replace or insert all specified tags
    for dcm_tag, tag_value in input_tags.tags_to_replace.items():
        if not dcm_tag in dataset:
            dataset.add_new(dcm_tag, datadict.dictionary_VR(dcm_tag), tag_value)
            logger.info(f"Add {dcm_tag}:{tag_value}")
        else:
            dataset[dcm_tag].value = tag_value
            logger.info(f"Update {dcm_tag}:{tag_value}")


def output_filepath(
    original_file_path: str, overwrite_output_file: bool = False
) -> str:
    """Generate the output filepath. If no overwrite, '_modified' is appended to the input. Otherwise, the input is returned
    Args:
        original_file_path (string) Path to the input file
        overwrite_option (boolean, optional) True to overwrite the input file
    """
    output_file_path = original_file_path
    if not overwrite_output_file:
        path_to_file = Path(original_file_path)
        output_file_path = (
            f"{path_to_file.parent}/{path_to_file.stem}_modified{path_to_file.suffix}"
        )
        logger.info(f"Output file: {output_file_path}")
    return output_file_path


def adjust_dicom_files(
    files: List[str],
    input_tags: parse_argument.InputTags,
    options: parse_argument.Options,
) -> None:
    """Adjust DICOM files according to rules and values passed as input

    Args:
        files ([str]): list of path to DICOM files
        input_tags (InputTags): Tags to replace/filled in the list of DICOM files
        options (Options): Options

    """
    update_data(input_tags)

    for file in files:
        logger.info(f"Work on file: {file}")
        try:
            dataset = dcmread(file)
        except (errors.InvalidDicomError, Exception) as error:
            logger.error(f"Invalid file to read: {file}: {error}")
            continue

        adjust_dicom_dataset(dataset, input_tags)
        try:
            output_file = output_filepath(file, options.overwrite_output_file)
            dataset.save_as(output_file)
        except Exception as error:
            logger.error(f"Can't write the DICOM file: {output_file}: {error}")
            continue


def fill_dcm_executable() -> None:
    """Main function that does the job"""

    command_line = argparse.ArgumentParser(
        prog="FillDCM",
        description="Tool to fill missing or empty DICOM tags or to replace others.",
    )
    command_line.add_argument(
        "files", metavar="dcm_file", nargs="+", help="List of DICOM files to edit"
    )
    command_line.add_argument(
        "-f",
        metavar="--fill-tag",
        action="append",
        dest="fill",
        help="DICOM tag to fill if missing or if its value is empty or undefined. A value to fill can be specified. Tag specification: <Tag name as a string>[=<value>]",
    )
    command_line.add_argument(
        "-r",
        metavar="--replace-tag",
        action="append",
        dest="replace",
        help="DICOM tag to replace with the specified value. If the tag doesn't exist, it is appended to the dataset. Tags specification: <Tag name as a string>=<value>",
    )
    command_line.add_argument(
        "-j",
        metavar="--json",
        dest="json_path",
        help='Specify a JSON file as input. This JSON file has a list of tags to fill or to replace. The expected structure for the JSON is: {"tags_to_fill":{}, "tags_to_replace":{}} with both attribute being dict of tags with value (or null)',
    )
    command_line.add_argument(
        "-ov",
        "--overwrite-file",
        action="store_true",
        help='Overwrite the original file. By default "_generated" is appended the the original filename and a new file is created.',
    )

    command_line.add_argument(
        "-v",
        "--verbose",
        dest="verbose_log",
        action="store_true",
        help="Enable verbose mode. More logs output.",
    )

    # TODO allow to pass tag as tag "0010,0010"

    input_args: argparse.Namespace = command_line.parse_args()
    try:
        input_tags, options = parse_argument.parse(input_args)
        logging.basicConfig(
            level=logging.DEBUG if options.verbose_log else logging.INFO,
            format="%(levelname)s - %(message)s",
        )
    except parse_argument.InvalidArgument as invalid_argument:
        command_line.error(f"Invalid argument: {invalid_argument}")

    try:
        parse_argument.verify_input_tags(input_tags)
        adjust_dicom_files(input_args.files, input_tags, options)
    except Exception as error:
        logger.error(f"Can't process an error encountered: {error}")
