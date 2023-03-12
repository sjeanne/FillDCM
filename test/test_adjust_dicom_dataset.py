import unittest
from pydicom import Dataset
from fill_dcm import adjust_dicom_dataset, generate_data

MANAGED_TAGS = ["PatientName", "PatientID", "PatientBirthDate",
                "ReferringPhysicianName", "DeviceSerialNumber"]


class TestAdjustDICOMDataset(unittest.TestCase):

    # TODO Why do we load a json file ? Can't we create a dataset in each test case ?
    def load_json_dataset(self, file_path):
        """ Helper function to load a Dataset from a JSON file

        Parameters:
            file_path (str) Path to the JSON file to load

        Returns:
            Loaded Dataset
        """
        ds = Dataset()
        with open(file_path, "r") as json_file:
            json_dataset = json_file.read()
        return ds.from_json(json_dataset)

    def test_missing_patient_name(self):
        """ Input dataset has no PatientName. Adjusted dataset shall have the replacement PatientName
        """
        ds = self.load_json_dataset("test/data/dcm_dataset_no_name.json")

        replacement_data = generate_data()

        self.assertFalse('PatientName' in ds)
        adjust_dicom_dataset(
            ds, replacement_data)

        self.assertTrue('PatientName' in ds)
        self.assertEqual(ds.PatientName, replacement_data["PatientName"])

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

    def test_missing_patient_id(self):
        """ Input dataset has no Patient ID (0010,0020). Adjusted dataset shall have the replacement Patient ID
        """
        ds = self.load_json_dataset("test/data/dcm_dataset_no_patient_id.json")

        replacement_data = generate_data()

        self.assertFalse('PatientID' in ds)
        adjust_dicom_dataset(ds, replacement_data)
        self.assertTrue('PatientID' in ds)
        self.assertEqual(ds.PatientID, replacement_data["PatientID"])

    def test_missing_referring_physician(self):
        """ use an empty Dataset without Referring Physician. Adjusted dataset shall have the replacement Referring Physician
        """
        ds = self.load_json_dataset(
            "test/data/dcm_dataset_no_referring_physician.json")

        replacement_data = generate_data()
        self.assertFalse('ReferringPhysicianName' in ds)
        adjust_dicom_dataset(ds, replacement_data)
        self.assertTrue('ReferringPhysicianName' in ds)
        self.assertEqual(ds.ReferringPhysicianName,
                         replacement_data["ReferringPhysicianName"])

    def test_missing_device_serial_number(self):
        """ use an empty Dataset without Device Serial Number. Adjusted dataset shall have the replacement Device Serial Number
        """
        ds = self.load_json_dataset(
            "test/data/dcm_dataset_no_device_serial_number.json")

        replacement_data = generate_data()
        self.assertFalse('DeviceSerialNumber' in ds)
        adjust_dicom_dataset(ds, replacement_data)
        self.assertTrue('DeviceSerialNumber' in ds)
        self.assertEqual(ds.DeviceSerialNumber,
                         replacement_data["DeviceSerialNumber"])

    def test_all_fields_empty(self):
        """ Input dataset contains all required tags but they are empty. All tags shall be adjusted.
        """
        ds = self.load_json_dataset(
            "test/data/dcm_dataset_all_empty.json")

        for dcm_tag in MANAGED_TAGS:
            self.assertEqual(ds[dcm_tag].VM, 0)

        replacement_data = generate_data()
        adjust_dicom_dataset(ds, replacement_data)

        for dcm_tag in MANAGED_TAGS:
            self.assertTrue(dcm_tag in ds)
            self.assertEqual(ds[dcm_tag].value, replacement_data[dcm_tag])

    def test_all_fields_missing(self):
        ds = Dataset()

        for dcm_tag in MANAGED_TAGS:
            self.assertFalse(dcm_tag in ds)

        replacement_data = generate_data()
        adjust_dicom_dataset(ds, replacement_data)

        for dcm_tag in MANAGED_TAGS:
            self.assertTrue(dcm_tag in ds)
            self.assertEqual(ds[dcm_tag].value, replacement_data[dcm_tag])

    def test_dataset_all_defined(self):
        """ Input dataset contains all required tags Patient Name, Patient ID, Patient Birthday, Referring Physician, Device Serial Number. Values shall not be modified.
        """
        ds = self.load_json_dataset(
            "test/data/dcm_dataset_all_defined.json")

        original_data = {}

        for dcm_tag in MANAGED_TAGS:
            self.assertTrue(dcm_tag in ds)
            original_data[dcm_tag] = ds[dcm_tag].value

        adjust_dicom_dataset(ds, generate_data())

        for dcm_tag in MANAGED_TAGS:
            self.assertTrue(dcm_tag in ds)
            self.assertEqual(ds[dcm_tag].value, original_data[dcm_tag])
