import unittest
from pydicom import Dataset
from fill_dcm import adjust_dicom_dataset, generate_data
from json import loads

MANAGED_TAGS = ["PatientName", "PatientID", "PatientBirthDate", "PatientSex",
                "ReferringPhysicianName", "DeviceSerialNumber"]


class TestAdjustDICOMDataset(unittest.TestCase):

    def load_dataset(self, json_dataset, tags_to_remove):
        json_ds = loads(json_dataset)
        for tag in tags_to_remove:
            if tag in json_ds:
                del json_ds[tag]

        ds = Dataset()
        return ds.from_json(json_ds)

    def test_missing_patient_name(self):
        """ Input dataset has no PatientName. Adjusted dataset shall have the replacement PatientName
        """
        ds = self.load_dataset(DICOM_DATASET_JSON, ["00100010"])

        replacement_data = generate_data()

        self.assertFalse('PatientName' in ds)
        adjust_dicom_dataset(
            ds, replacement_data)

        self.assertTrue('PatientName' in ds)
        self.assertEqual(ds.PatientName, replacement_data["PatientName"])

    def test_missing_birth_date(self):
        """ Input dataset has no PatientBirthDate. Adjusted dataset shall have the replacement PatientBirthDate
        """
        ds = self.load_dataset(DICOM_DATASET_JSON, ["00100030"])

        replacement_data = generate_data()

        self.assertFalse('PatientBirthDate' in ds)
        adjust_dicom_dataset(ds, replacement_data)
        self.assertTrue('PatientBirthDate' in ds)
        self.assertEqual(ds.PatientBirthDate,
                         replacement_data["PatientBirthDate"])

    def test_missing_patient_id(self):
        """ Input dataset has no Patient ID (0010,0020). Adjusted dataset shall have the replacement Patient ID
        """
        ds = self.load_dataset(DICOM_DATASET_JSON, ["00100020"])

        replacement_data = generate_data()

        self.assertFalse('PatientID' in ds)
        adjust_dicom_dataset(ds, replacement_data)
        self.assertTrue('PatientID' in ds)
        self.assertEqual(ds.PatientID, replacement_data["PatientID"])

    def test_missing_patient_sex(self):
        """ Input dataset has no PatientSex. Adjusted dataset shall have the replacement PatientSex
        """
        ds = self.load_dataset(DICOM_DATASET_JSON, ["00100040"])

        replacement_data = generate_data()

        self.assertFalse('PatientSex' in ds)
        adjust_dicom_dataset(
            ds, replacement_data)

        self.assertTrue('PatientSex' in ds)
        self.assertEqual(ds.PatientSex, replacement_data["PatientSex"])

    def test_missing_referring_physician(self):
        """ use an empty Dataset without Referring Physician. Adjusted dataset shall have the replacement Referring Physician
        """
        ds = self.load_dataset(DICOM_DATASET_JSON, ["00080090"])

        replacement_data = generate_data()
        self.assertFalse('ReferringPhysicianName' in ds)
        adjust_dicom_dataset(ds, replacement_data)
        self.assertTrue('ReferringPhysicianName' in ds)
        self.assertEqual(ds.ReferringPhysicianName,
                         replacement_data["ReferringPhysicianName"])

    def test_missing_device_serial_number(self):
        """ use an empty Dataset without Device Serial Number. Adjusted dataset shall have the replacement Device Serial Number
        """
        ds = self.load_dataset(DICOM_DATASET_JSON, ["00181000"])

        replacement_data = generate_data()
        self.assertFalse('DeviceSerialNumber' in ds)
        adjust_dicom_dataset(ds, replacement_data)
        self.assertTrue('DeviceSerialNumber' in ds)
        self.assertEqual(ds.DeviceSerialNumber,
                         replacement_data["DeviceSerialNumber"])

    def test_all_fields_empty(self):
        """ Input dataset contains all required tags but they are empty. All tags shall be adjusted.
        """
        ds = self.load_dataset(DICOM_DATASET_JSON, [])
        for dcm_tag in MANAGED_TAGS:
            ds[dcm_tag].clear()

        for dcm_tag in MANAGED_TAGS:
            self.assertEqual(ds[dcm_tag].VM, 0)

        replacement_data = generate_data()
        adjust_dicom_dataset(ds, replacement_data)

        for dcm_tag in MANAGED_TAGS:
            self.assertTrue(dcm_tag in ds)
            self.assertEqual(ds[dcm_tag].value, replacement_data[dcm_tag])

    def test_all_fields_missing(self):
        """ Input dataset contains none of the required  tags. All tags shall be filled with a value.
        """
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
        ds = self.load_dataset(DICOM_DATASET_JSON, [])

        original_data = {}

        for dcm_tag in MANAGED_TAGS:
            self.assertTrue(dcm_tag in ds)
            original_data[dcm_tag] = ds[dcm_tag].value

        adjust_dicom_dataset(ds, generate_data())

        for dcm_tag in MANAGED_TAGS:
            self.assertTrue(dcm_tag in ds)
            self.assertEqual(ds[dcm_tag].value, original_data[dcm_tag])


DICOM_DATASET_JSON = r"""{
    "00080005": { "Value": ["ISO_IR 100"], "vr": "CS" },
    "00080008": {
        "Value": ["ORIGINAL", "PRIMARY", "OTHER", "R", "IR"],
        "vr": "CS"
    },
    "00080012": { "Value": ["19960823"], "vr": "DA" },
    "00080013": { "Value": ["093801"], "vr": "TM" },
    "00080014": { "Value": ["1.3.46.670589.11.0.5"], "vr": "UI" },
    "00080016": { "Value": ["1.2.840.10008.5.1.4.1.1.4"], "vr": "UI" },
    "00080018": {
        "Value": ["1.3.46.670589.11.0.4.1996082307380006"],
        "vr": "UI"
    },
    "00080090": {
        "Value": [{ "Alphabetic": "Referring^Phy" }],
        "vr": "PN"
    },
    "00100010": {
        "Value": [{ "Alphabetic": "LastName^FirstName" }],
        "vr": "PN"
    },
    "00100020": { "Value": ["7"], "vr": "LO" },
    "00100030": { "Value": ["19010101"], "vr": "DA" },
    "00100040": { "Value": ["M"], "vr": "CS" },
    "00101030": { "Value": [90.0], "vr": "DS" },
    "00181000": { "Value": ["00000"], "vr": "LO" }
}"""
