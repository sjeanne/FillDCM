import unittest
from pydicom import Dataset
from fill_dcm import adjust_dicom_dataset, generate_data


class TestAdjustDICOMDataset(unittest.TestCase):

    def load_json_dataset(self, file_path):
        ds = Dataset()
        with open(file_path, "r") as json_file:
            json_dataset = json_file.read()
        return ds.from_json(json_dataset)

    def test_missing_name(self):
        """ Input dataset has no PatientName. Adjusted dataset shall have the replacement PatientName
        """
        ds = self.load_json_dataset("test/data/dcm_dataset_no_name.json")

        replacement_data = generate_data()

        self.assertFalse('PatientName' in ds)
        adjust_dicom_dataset(
            ds, replacement_data)

        self.assertTrue('PatientName' in ds)
        self.assertEqual(ds.PatientName, replacement_data["PatientName"])

    def test_name_exist(self):
        """ Input dataset already has a patientName. Output dataset shall have the original PatientName
        """
        ds = self.load_json_dataset(
            "test/data/dcm_dataset_with_patientname.json")
        self.assertTrue('PatientName' in ds)
        current_patient_name = ds.PatientName

        adjust_dicom_dataset(ds, generate_data())

        self.assertTrue('PatientName' in ds)
        self.assertEqual(ds.PatientName, current_patient_name)

    def test_missing_birth_date(self):
        """ Input dataset has no PatientBirthDate. Adjusted dataset shall have the replacement PatientBirthDate
        """
        ds = self.load_json_dataset("test/data/dcm_dataset_no_birthdate.json")

        replacement_data = generate_data()

        self.assertFalse('PatientBirthDate' in ds)
        adjust_dicom_dataset(ds, replacement_data)
        self.assertTrue('PatientBirthDate' in ds)
        self.assertEqual(ds.PatientBirthDate,
                         replacement_data["PatientBirthDate"])
