import argparse
import pydicom
import string
from random import randrange, choices
from enum import Enum, auto
from pathlib import Path


class Gender(Enum):
    MALE = auto()
    FEMALE = auto()
    NOT_SPECIFIED = auto()


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


def generate_data(input_values={}, patient_gender=Gender.NOT_SPECIFIED):
    """ Generate a structure filled with data used to fill missing/incomplete tags.
        Data can either be generated or specified by the caller
        Parameters:
            input_values (obj) Values defined by the caller
            patient_gender (Gender) Used to generate PatientName
    """
    return {"PatientName": input_values["patient_name"] if ("patient_name" in input_values) else generate_personal_name(patient_gender),
            "ReferringPhysicianName": input_values["referring_physician_name"] if ("referring_physician_name" in input_values) else generate_personal_name(),
            "PatientBirthDate": input_values["patient_birthdate"] if "patient_birthdate" in input_values else generate_date(),
            "PatientID": input_values["patient_id"] if "patient_id" in input_values else generate_id(),
            "DeviceSerialNumber": input_values["device_serial_number"] if "device_serial_number" in input_values else generate_id()
            }


def generate_id():
    """ Generate a Patient ID following DICOM LO VR spec
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Patient ID is generated as: XXYYYY where X is a
    Returns:
        A Patient ID as a string
    """
    return "".join(choices(string.ascii_uppercase + string.digits, k=10))


def generate_personal_name(gender=Gender.NOT_SPECIFIED):
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
    return "{}^{}".format(choices(PERSONAL_NAME_SAMPLE["last_names"])[0], choices(possible_first_names)[0])


def generate_date():
    """ Generate a data and follow DICOM DA VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
        Returns:
            A DICOM date
        """
    return "{}{:02}{:02}".format(randrange(1950, 2020), randrange(1, 12), randrange(1, 30))


def is_tag_empty_or_missing(tag_name, dataset):
    """ Check if the tag is missing or has an empty value
        Parameters:
            tag_name (string) Tag to find
            dataset (Dataset) Dataset
        Returns:
            True if the tag is missing or empty, otherwise False
    """
    return not (tag_name in dataset) or dataset[tag_name].VM == 0


def adjust_dicom_dataset(dataset, replacement_data):
    # TODO more generic code
    if is_tag_empty_or_missing('PatientName', dataset):
        dataset.PatientName = replacement_data["PatientName"]
    if is_tag_empty_or_missing('ReferringPhysicianName', dataset):
        dataset.ReferringPhysicianName = replacement_data["ReferringPhysicianName"]
    if is_tag_empty_or_missing('PatientBirthDate', dataset):
        dataset.PatientBirthDate = replacement_data["PatientBirthDate"]
    if is_tag_empty_or_missing('PatientID', dataset):
        dataset.PatientID = replacement_data["PatientID"]
    if is_tag_empty_or_missing('DeviceSerialNumber', dataset):
        dataset.DeviceSerialNumber = replacement_data["DeviceSerialNumber"]


def output_filepath(original_file_path, overwrite_option):
    """ Generate the output filepath. If no overwrite, '_modified' is appended to the input. Otherwise, the input is returned
    Args:
        original_file_path (string) Path to the input file
        overwrite_option (boolean) True to overwrite the input file
    """
    output_filepath = original_file_path
    if not overwrite_option:
        path_to_file = Path(original_file_path)
        output_filepath = "{}/{}_modified{}".format(
            path_to_file.parent, path_to_file.stem, path_to_file.suffix)
    return output_filepath


def adjust_dicom_files(files, input_values, options):
    """ Adjust DICOM files according to rules and values passed as input

    Args:
        files ([str]): list of path to DICOM files
        input_values (obj): Values to set into DICOM files
        options (obj): Options passed to configure behaviors
    Exceptions:

    """
    try:
        patient_sex_dataset = pydicom.dcmread(
            files[0], specific_tags=['PatientSex'])
        patient_gender = Gender.MALE if patient_sex_dataset.PatientSex == 'M' else Gender.FEMALE
    except:
        print("Invalid file to read: {}".format(files[0]))
        return

    replacement_data = generate_data(input_values, patient_gender)

    for file in files:
        print("Work on file: {}".format(file))
        try:
            dataset = pydicom.dcmread(file)
        except:
            print("Invalid file to read: {}".format(file))

        adjust_dicom_dataset(dataset, replacement_data)
        dataset.save_as(output_filepath(file, options["overwrite_inputs"]))


def fill_dcm_executable():
    command_line = argparse.ArgumentParser(
        prog="FillDCM",
        description="",
    )
    command_line.add_argument(
        'files', metavar='dcm_file', nargs='+', help="DICOM files to edit")
    command_line.add_argument(
        '-pn', '--patient-name', help='Patient name to set. Shall follow PN VR from the DICOM standard.')
    command_line.add_argument(
        '-pbd', '--patient-birthdate', help='Patient birthdate to set. Shall follow DA VR from the DICOM standard.')
    command_line.add_argument(
        '-pid', '--patient-id', help='Patient ID to set. Shall follow LO VR from the DICOM standard.')
    command_line.add_argument(
        '-rfn', '--referring-physician-name', help='Referring Physician name to set. Shall follow PN VR from the DICOM standard.')
    command_line.add_argument(
        '-dsn', '--device-serial-number', help='Device Serial Number to set. Shall follow LO VR from the DICOM standard.')
    command_line.add_argument(
        '-ov', '--overwrite',
        action='store_true',
        help='Overwrite the original file. By default "_generated" is append the the original filename and a new file is created.')

    input_args = command_line.parse_args()
    adjust_dicom_files(files=input_args.files, input_values={
                       "patient_name": input_args.patient_name}, options={"overwrite_inputs": input_args.overwrite})


if __name__ == '__main__':
    fill_dcm_executable()
