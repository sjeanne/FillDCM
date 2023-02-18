import argparse
import pydicom
import string
from random import randrange, choices


def generate_data():
    return {"PatientName": generate_personal_name(),
            "ReferringPhysicianName": generate_personal_name(),
            "PatientBirthDate": generate_date(),
            "PatientID": generate_id(),
            "DeviceSerialNumber": generate_id()
            }


def generate_id():
    """ Generate a Patient ID following DICOM LO VR spec
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Patient ID is generated as: XXYYYY where X is a
    Returns:
        A Patient ID as a string
    """
    return "".join(choices(string.ascii_uppercase + string.digits, k=10))


def generate_personal_name():
    """ Generate a personal name and follow DICOM PN VR spec.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Only first and last names are filled.

    Returns:
        A DICOM personal name
    """
    return "Last^First"


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
    if (tag_name in dataset and dataset[tag_name].VM == 0):
        print("Empty tag:", tag_name, dataset[tag_name])
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


def adjust_dicom_files(files, input_values):
    """ Adjust DICOM files according to rules and values passed as input

    Args:
        files ([str]): list of path to DICOM files
        input_values (obj): Values to set into DICOM files
Raises:
    """

    replacement_data = generate_data()
    for file in files:
        print("Work on file: {}".format(file))
        dataset = pydicom.dcmread(file)
        adjust_dicom_dataset(dataset, replacement_data)
        dataset.save_as("new_file.dcm")


def fill_dcm_executable():
    command_line = argparse.ArgumentParser(
        prog="DCMAdjust",
        description="",
        # exit_on_error=False
    )
    command_line.add_argument(
        'files', metavar='dcm_file', nargs='+', help="DICOM files to edit")
    command_line.add_argument(
        '-p', '--patient-name', help='Patient name to set. Shall follow PN VR from the DICOM standard.')
    # TODO Add Patient's birthdate
    # TODO Add Patient's ID
    # TODO Add Referring Physician
    # TODO Add Device serial number
    # TODO Add option to not over write input files, shall be default behavior

    input_args = command_line.parse_args()
    adjust_dicom_files(files=input_args.files, input_values={
                       "patient_name": input_args.patient_name})


if __name__ == '__main__':
    fill_dcm_executable()
