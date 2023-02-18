import unittest
from pydicom import Dataset
from fill_dcm import adjust_dicom_dataset, generate_data


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

        # TODO can be written in a more generic way

        self.assertEqual(ds['PatientName'].VM, 0)
        self.assertEqual(ds['PatientID'].VM, 0)
        self.assertEqual(ds['PatientBirthDate'].VM, 0)
        self.assertEqual(ds['ReferringPhysicianName'].VM, 0)
        self.assertEqual(ds['DeviceSerialNumber'].VM, 0)

        replacement_data = generate_data()
        adjust_dicom_dataset(ds, replacement_data)

        self.assertTrue('PatientName' in ds)
        self.assertEqual(ds.PatientName,
                         replacement_data["PatientName"])
        self.assertTrue('PatientID' in ds)
        self.assertEqual(ds.PatientID, replacement_data["PatientID"])
        self.assertTrue('PatientBirthDate' in ds)
        self.assertEqual(ds.PatientBirthDate,
                         replacement_data["PatientBirthDate"])
        self.assertTrue('ReferringPhysicianName' in ds)
        self.assertEqual(ds.ReferringPhysicianName,
                         replacement_data["ReferringPhysicianName"])
        self.assertTrue('DeviceSerialNumber' in ds)
        self.assertEqual(ds.DeviceSerialNumber,
                         replacement_data["DeviceSerialNumber"])

    def test_all_fields_missing(self):
        # TODO can be written in a more generic way

        ds = Dataset()
        self.assertFalse('PatientName' in ds)
        self.assertFalse('PatientID' in ds)
        self.assertFalse('PatientBirthDate' in ds)
        self.assertFalse('ReferringPhysicianName' in ds)
        self.assertFalse('DeviceSerialNumber' in ds)

        replacement_data = generate_data()
        adjust_dicom_dataset(ds, replacement_data)

        self.assertTrue('PatientName' in ds)
        self.assertEqual(ds.PatientName,
                         replacement_data["PatientName"])
        self.assertTrue('PatientID' in ds)
        self.assertEqual(ds.PatientID, replacement_data["PatientID"])
        self.assertTrue('PatientBirthDate' in ds)
        self.assertEqual(ds.PatientBirthDate,
                         replacement_data["PatientBirthDate"])
        self.assertTrue('ReferringPhysicianName' in ds)
        self.assertEqual(ds.ReferringPhysicianName,
                         replacement_data["ReferringPhysicianName"])
        self.assertTrue('DeviceSerialNumber' in ds)
        self.assertEqual(ds.DeviceSerialNumber,
                         replacement_data["DeviceSerialNumber"])

    def test_dataset_all_defined(self):
        """ Input dataset contains all required tags Patient Name, Patient ID, Patient Birthday, Referring Physician, Device Serial Number. Values shall not be modified.
        """
        ds = self.load_json_dataset(
            "test/data/dcm_dataset_all_defined.json")

        # TODO can be written in a more generic way
        self.assertTrue('PatientName' in ds)
        patient_name = ds.PatientName
        self.assertTrue('PatientID' in ds)
        patient_id = ds.PatientID
        self.assertTrue('PatientBirthDate' in ds)
        patient_birthdate = ds.PatientBirthDate
        self.assertTrue('ReferringPhysicianName' in ds)
        referring_physician_name = ds.ReferringPhysicianName
        self.assertTrue('DeviceSerialNumber' in ds)
        device_serial_number = ds.DeviceSerialNumber

        adjust_dicom_dataset(ds, generate_data())

        self.assertTrue('PatientName' in ds)
        self.assertEqual(ds.PatientName, patient_name)
        self.assertTrue('PatientID' in ds)
        self.assertEqual(patient_id, ds.PatientID)
        self.assertTrue('PatientBirthDate' in ds)
        self.assertEqual(ds.PatientBirthDate, patient_birthdate)
        self.assertTrue('ReferringPhysicianName' in ds)
        self.assertEqual(ds.ReferringPhysicianName, referring_physician_name)
        self.assertTrue('DeviceSerialNumber' in ds)
        self.assertEqual(ds.DeviceSerialNumber,
                         device_serial_number)

    # TODO adjust test to manage a Dataset with all filed defined
