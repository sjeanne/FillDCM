""" fill_dcm
"""

import argparse
import string
from random import randrange, choices
from enum import Enum
from pathlib import Path
from pydicom import dcmread, datadict, errors


class Gender(str, Enum):
    """ Gender enum 
    """
    MALE = 'M'
    FEMALE = 'F'
    NOT_SPECIFIED = 'O'


class InvalidParameter(Exception):
    """ Exception to handle CLI parameter errors
    """


PERSONAL_NAME_SAMPLE = {
    "first_names_male": ["James",
                         "Robert",
                         "John",
                         "Michael",
                         "David",
                         "William",
                         "Richard",
                         "Joseph",
                         "Thomas",
                         "Charles",
                         "Christopher",
                         "Daniel",
                         "Matthew",
                         "Anthony",
                         "Mark",
                         "Donald",
                         "Steven",
                         "Paul",
                         "Andrew",
                         "Joshua",
                         "Kenneth",
                         "Kevin",
                         "Brian",
                         "George",
                         "Timothy",
                         "Ronald",
                         "Edward",
                         "Jason",
                         "Jeffrey",
                         "Ryan",
                         "Jacob",
                         "Gary",
                         "Nicholas",
                         "Eric",
                         "Jonathan",
                         "Stephen",
                         "Larry",
                         "Justin",
                         "Scott",
                         "Brandon",
                         "Benjamin",
                         "Samuel",
                         "Gregory",
                         "Alexander",
                         "Frank",
                         "Patrick",
                         "Raymond",
                         "Jack",
                         "Dennis",
                         "Jerry",
                         "Tyler",
                         "Aaron",
                         "Jose",
                         "Adam",
                         "Nathan",
                         "Henry"],
    "first_names_female": ["Mary",
                           "Patricia",
                           "Jennifer",
                           "Linda",
                           "Elizabeth",
                           "Barbara",
                           "Susan",
                           "Jessica",
                           "Sarah",
                           "Karen",
                           "Lisa",
                           "Nancy",
                           "Betty",
                           "Margaret",
                           "Sandra",
                           "Ashley",
                           "Kimberly",
                           "Emily",
                           "Donna",
                           "Michelle",
                           "Carol",
                           "Amanda",
                           "Dorothy",
                           "Melissa",
                           "Deborah",
                           "Stephanie",
                           "Rebecca",
                           "Sharon",
                           "Laura",
                           "Cynthia",
                           "Kathleen",
                           "Amy",
                           "Angela",
                           "Shirley",
                           "Anna",
                           "Brenda",
                           "Pamela",
                           "Emma",
                           "Nicole",
                           "Helen",
                           "Samantha",
                           "Katherine",
                           "Christine",
                           "Debra",
                           "Rachel",
                           "Carolyn",
                           "Janet",
                           "Catherine",
                           "Maria",
                           "Heather",
                           "Diane",
                           "Ruth",
                           "Julie",
                           "Olivia",
                           "Joyce",
                           "Virginia"],
    "last_names": ["Smith",
                   "Johnson",
                   "Williams",
                   "Brown",
                   "Jones",
                   "Garcia",
                   "Miller",
                   "Davis",
                   "Rodriguez",
                   "Martinez",
                   "Hernandez",
                   "Lopez",
                   "Gonzalez",
                   "Wilson",
                   "Anderson",
                   "Thomas",
                   "Taylor",
                   "Moore",
                   "Jackson",
                   "Martin",
                   "Lee",
                   "Perez",
                   "Thompson",
                   "White",
                   "Harris",
                   "Sanchez",
                   "Clark",
                   "Ramirez",
                   "Lewis",
                   "Robinson",
                   "Walker",
                   "Young",
                   "Allen",
                   "King",
                   "Wright",
                   "Scott",
                   "Torres",
                   "Nguyen",
                   "Hill",
                   "Flores",
                   "Green",
                   "Adams",
                   "Nelson",
                   "Baker",
                   "Hall",
                   "Rivera",
                   "Campbell",
                   "Mitchell",
                   "Carter",
                   "Roberts"]
}


def dicom_sex_to_gender(dcm_sex: str = ''):
    """ Convert DICOM CS Sex values to Gender enum
    """
    match dcm_sex:
        case 'M':
            return Gender.MALE
        case 'F':
            return Gender.FEMALE
        case _:
            return Gender.NOT_SPECIFIED


def update_data(input_values):
    """ Define a value to each tag without. The generated value matches tag's VR. 
        If a tag has a defined value, it is not updated.
        Parameters:
            input_values (obj) Values defined by the caller
    """
    if input_values["tags"] is not None:
        for tag in input_values["tags"]:
            if input_values["tags"][tag] is None:
                tag_vr = datadict.dictionary_VR(tag)
                match(tag_vr):
                    case 'AS':
                        input_values["tags"][tag] = generate_age_string()
                    case    'SH', 'ST', 'TM', 'UI', 'US':
                        raise InvalidParameter(
                            f"VR: {tag_vr} for tag {tag} not managed")
                    case 'DA':
                        input_values["tags"][tag] = generate_date()
                    case 'DS':
                        input_values["tags"][tag] = generate_decimal_string()
                    case 'DT':
                        input_values["tags"][tag] = generate_date_time()
                    case 'IS':
                        input_values["tags"][tag] = generate_integer_string()
                    case 'LO':
                        input_values["tags"][tag] = generate_lo()
                    case 'LT':
                        input_values["tags"][tag] = generate_long_text()
                    case 'PN':
                        input_values["tags"][tag] = generate_personal_name()
                    case _:
                        raise InvalidParameter(
                            f"VR: {tag_vr} for tag {tag} not managed")
    return input_values


def generate_id() -> str:
    """ Generate a Patient ID following DICOM LO VR spec
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Patient ID is generated as: XXYYYY where X is a
    Returns:
        A Patient ID as a string
    """
    return "".join(choices(string.ascii_uppercase + string.digits, k=10))


def generate_age_string() -> str:
    """Generate an Age String and follows DICOM AS VR spec.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Only ages in years are generated: "XXXY" where 'X' are digits characters

    Returns:
        A DICOM Age String
    """
    return "".join(choices(string.digits, k=3)+["Y"])


def generate_decimal_string() -> str:
    """Generate a Decimal String and follows DICOM DS VR spec.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Only fixed point numbers are generating: only digits from 1 to 16 bytes

    Returns:
        A DICOM Decimal String
    """
    return "".join(choices(string.digits, k=randrange(1, 16)))


def generate_date_time() -> str:
    """Generate a Date Time and follows DICOM DT VR spec.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Only the following fields from DT are filled: YYYYMMDDHHMMSS

    Returns:
        A DICOM Date Time
    """
    return f"{generate_date()}{randrange(0, 23):02}{randrange(0, 59):02}{randrange(0, 59):02}"


def generate_integer_string() -> str:
    """ Generate a Integer String and follows DICOM IS VR spec.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Generate Integer in the range -2^31 <= n <= 2^31-1

    Returns:
        str: Integer string
    """
    return f"{randrange(-1*2**31, (2**31)-1)}"


def generate_personal_name(gender=Gender.NOT_SPECIFIED) -> str:
    """ Generate a personal name and follow DICOM PN VR spec.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Only first and last names are filled.

    Returns:
        A DICOM personal name
    """
    possible_first_names = []
    if gender == Gender.FEMALE:
        possible_first_names = PERSONAL_NAME_SAMPLE["first_names_female"]
    elif gender == Gender.MALE:
        possible_first_names = PERSONAL_NAME_SAMPLE["first_names_male"]
    else:
        possible_first_names.extend(PERSONAL_NAME_SAMPLE["first_names_female"])
        possible_first_names.extend(PERSONAL_NAME_SAMPLE["first_names_male"])
    return f"{choices(PERSONAL_NAME_SAMPLE['last_names'])[0]}^{choices(possible_first_names)[0]}"


def generate_date():
    """ Generate a data and follow DICOM DA VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Years are in range [1950, 2020]
        Returns:
            A DICOM date
        """
    return f"{randrange(1950, 2020)}{randrange(1, 12):02}{randrange(1, 30):02}"


def generate_lo():
    """ Generate a data and follow DICOM LO VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
        Returns:
            A randomized LO value with at least one character and max 64
    """
    return "".join(choices(string.ascii_letters + string.digits, k=randrange(1, 64)))


def generate_long_text():
    """ Generate a data and follow DICOM LT VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
        Returns:
            A randomized LT value with at least one character and max 1024
    """
    return "".join(choices(string.ascii_letters + string.digits, k=randrange(1, 1024)))


def adjust_dicom_dataset(dataset, input_tags):
    """ Replace in the dataset empty or missing tags by replacement data
        Parameters:
            dataset (Dataset) Dataset to adjust
            input_tags (object) Data used to replace or overwrite DICOM tags
    """
    # Replace only empty/missing  DICOM tags
    if input_tags["tags"] is not None:
        for dcm_tag, tag_value in input_tags["tags"].items():
            if not dcm_tag in dataset:
                dataset.add_new(dcm_tag, datadict.dictionary_VR(
                    dcm_tag), tag_value)
            elif dataset[dcm_tag].VM == 0:
                dataset[dcm_tag].value = tag_value

    # Overwrite or insert all specified tags
    if input_tags["tags_to_overwrite"] is not None:
        for dcm_tag, tag_value in input_tags["tags_to_overwrite"].items():
            if not dcm_tag in dataset:
                dataset.add_new(dcm_tag, datadict.dictionary_VR(
                    dcm_tag), tag_value)
            else:
                dataset[dcm_tag].value = tag_value


def output_filepath(original_file_path, overwrite_option=False):
    """ Generate the output filepath. If no overwrite, '_modified' is appended to the input. Otherwise, the input is returned
    Args:
        original_file_path (string) Path to the input file
        overwrite_option (boolean) True to overwrite the input file
    """
    output_file_path = original_file_path
    if not overwrite_option:
        path_to_file = Path(original_file_path)
        output_file_path = f"{path_to_file.parent}/{path_to_file.stem}_modified{path_to_file.suffix}"
    return output_file_path


def adjust_dicom_files(files, input_tags):
    """ Adjust DICOM files according to rules and values passed as input

    Args:
        files ([str]): list of path to DICOM files
        input_tags (obj): Tags to replace/filled in the list of DICOM files

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
        # TODO bring back option mechanism to overwrite output file
        dataset.save_as(output_filepath(file))
        # , options["overwrite_inputs"]))


def tag_is_in_dicom_dictionary(tag: str) -> bool:
    """ Indicated if a tag, by its string value, exist in the DICOM dictionary

    Args:
        tag (str): Tag name to verify

    Returns:
        bool: True if tag exists, otherwise False
    """
    return datadict.dictionary_has_tag(tag)


def verify_input_tags(input_args):
    """ Verify validity of inputs arguments. Rules:
        - a tag can't be in both list (tag and tag to overwrite)
        - a tag to overwrite must have a value (e.g "tag=value")
        - at least one tag shall be provided
        - tags of both lists must be a valid tag from DICOM dictionary
    Exceptions:
        InvalidParameter if a condition is not matched
    """
    # At least one tag shall be defined
    if len(input_args["tags"].keys()) == 0 and len(input_args["tags_to_overwrite"].keys()) == 0:
        raise InvalidParameter("At least one tag shall be defined")

    # Duplication between the two lists of tags
    # and Tags to overwrite must have a value
    # and Tags to overwrite shall be in DICOM dictionary
    if "tags_to_overwrite" in input_args and input_args["tags_to_overwrite"] is not None:
        for tag_to_overwrite in input_args["tags_to_overwrite"]:
            if input_args["tags_to_overwrite"][tag_to_overwrite] is None:
                raise InvalidParameter(
                    f"Tag {tag_to_overwrite} must have value.")
            if tag_to_overwrite in input_args["tags"]:
                raise InvalidParameter(
                    f"Tag {tag_to_overwrite} is duplicated. A tag can only be defined once")
            if not tag_is_in_dicom_dictionary(tag_to_overwrite):
                raise InvalidParameter(
                    f"Tag {tag_to_overwrite} is not a valid tag from DICOM dictionary")

    # tags shall be in DICOM dictionary
    if "tags" in input_args and input_args["tags"] is not None:
        for tag in input_args["tags"]:
            if not tag_is_in_dicom_dictionary(tag):
                raise InvalidParameter(
                    f"Tag {tag} is not a valid tag from DICOM dictionary")

    # TODO verify that values passed are correct according to  tag's VR


def parse_arguments(input_args):
    """ Parse input arguments and return two dictionaries of tag and tag_to_overwrite
    """
    parsed_tags = dict([("tags", {}), ("tags_to_overwrite", {})])
    # tags
    if "t" in input_args and input_args.t is not None:
        for raw_tag in input_args.t:
            splitted_tag = raw_tag.split("=", 1)
            parsed_tags["tags"][splitted_tag[0]] = None if len(
                splitted_tag) == 1 else splitted_tag[1]

    # tags to overwrite
    if "to" in input_args and input_args.to is not None:
        for raw_tag_to_overwrite in input_args.to:
            splitted_tag = raw_tag_to_overwrite.split("=", 1)
            parsed_tags["tags_to_overwrite"][splitted_tag[0]] = None if len(
                splitted_tag) == 1 else splitted_tag[1]

    return parsed_tags


def fill_dcm_executable():
    command_line = argparse.ArgumentParser(
        prog="FillDCM",
        description="Do stuff",
    )
    command_line.add_argument(
        'files', metavar='dcm_file', nargs='+', help="DICOM files to edit")
    command_line.add_argument('-t', metavar='--tag', action='append',
                              help="DICOM tag to fill if value is empty or undefined")
    command_line.add_argument('-to', metavar='--tag-overwrite', action='append',
                              help="DICOM tag to overwrite with the specified value")
    # TODO: add output options

    input_args = command_line.parse_args()
    print(input_args)
    input_tags = parse_arguments(input_args)
    print(input_tags)
    verify_input_tags(input_tags)

    adjust_dicom_files(input_args.files, input_tags)


if __name__ == '__main__':
    fill_dcm_executable()
