import argparse
import pydicom
from random import randrange


def generate_data():
    return {"PatientName": generate_personal_name(),
            "ReferingPhysician": generate_personal_name(),
            "PatientBirthDate": generate_date()
            }


def generate_personal_name():
    """ Generate a personal name and follow DICOM PN VR spec.
    Only first and last names are filled.

    Returns:
        A DICOM personal name
    """
    return "Last^First"


def generate_date():
    """ Generate a data and follow DICOM DA VR specs.
        Returns:
            A DICOM date
        """
    return "{}{:02}{:02}".format(randrange(1950, 2020), randrange(1, 12), randrange(1, 30))


def adjust_dicom_dataset(dataset, replacement_data):
    if not ('PatientName' in dataset):
        dataset.PatientName = replacement_data["PatientName"]
    if not ('ReferingPhysician' in dataset):
        dataset.ReferingPhysician = replacement_data["ReferingPhysician"]
    if not ('PatientBirthDate' in dataset):
        dataset.PatientBirthDate = replacement_data["PatientBirthDate"]


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
    # TODO Add Refering Physician
    # TODO Add Device serial number
    # TODO Add option to not over write input files, shall be default behaviour

    input_args = command_line.parse_args()
    adjust_dicom_files(files=input_args.files, input_values={
                       "patient_name": input_args.patient_name})


if __name__ == '__main__':
    fill_dcm_executable()
