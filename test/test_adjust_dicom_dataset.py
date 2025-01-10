"""Unit test
"""

import unittest
from json import loads

from pydicom import Dataset

from fill_dcm import fill_dcm, parse_argument


class TestAdjustDICOMDataset(unittest.TestCase):

    def load_dataset(self, json_dataset, tags_to_remove):
        """Load a DICOM dataset from a JSON payload"""
        json_ds = loads(json_dataset)
        for tag in tags_to_remove:
            if tag in json_ds:
                del json_ds[tag]

        ds = Dataset()
        return ds.from_json(json_ds)

    def test_missing_patient_name(self):
        """Input dataset has no PatientName and PatientName is a tag to fill. Adjusted dataset shall have the replacement PatientName"""
        ds = self.load_dataset(DICOM_DATASET_JSON, tags_to_remove=["00100010"])
        replacement_data = fill_dcm.update_data(parse_argument.InputTags({"PatientName": None}, {}))

        self.assertFalse("PatientName" in ds)
        fill_dcm.adjust_dicom_dataset(ds, replacement_data)

        self.assertTrue("PatientName" in ds)
        self.assertEqual(ds.PatientName, replacement_data.tags_to_fill["PatientName"])

    def test_missing_patient_name_specified(self):
        """Input dataset has no PatientName and PatientName is a tag to fill with a specified value. Adjusted dataset shall have the specified PatientName"""
        ds = self.load_dataset(DICOM_DATASET_JSON, tags_to_remove=["00100010"])

        patient_name = "Hampton^Fredrick"
        replacement_data = fill_dcm.update_data(parse_argument.InputTags({"PatientName": patient_name}, {}))

        self.assertEqual(patient_name, replacement_data.tags_to_fill["PatientName"])
        self.assertFalse("PatientName" in ds)
        fill_dcm.adjust_dicom_dataset(ds, replacement_data)

        self.assertTrue("PatientName" in ds)
        self.assertEqual(ds.PatientName, replacement_data.tags_to_fill["PatientName"])

    def test_missing_birth_date(self):
        """Input dataset has no PatientBirthDate and PatientBirthDate is a tag to fill. Adjusted dataset shall have the replacement PatientBirthDate"""
        ds = self.load_dataset(DICOM_DATASET_JSON, tags_to_remove=["00100030"])

        replacement_data = fill_dcm.update_data(parse_argument.InputTags({"PatientBirthDate": None}, {}))

        self.assertFalse("PatientBirthDate" in ds)
        fill_dcm.adjust_dicom_dataset(ds, replacement_data)
        self.assertTrue("PatientBirthDate" in ds)
        self.assertEqual(ds.PatientBirthDate, replacement_data.tags_to_fill["PatientBirthDate"])

    def test_missing_birth_date_specified(self):
        """Input dataset has no PatientBirthDate and PatientBirthDate is a tag to fill with specified value. Adjusted dataset shall have the specified PatientBirthDate"""
        ds = self.load_dataset(DICOM_DATASET_JSON, tags_to_remove=["00100030"])

        patient_dob = "19480830"
        replacement_data = fill_dcm.update_data(parse_argument.InputTags({"PatientBirthDate": patient_dob}, {}))

        self.assertEqual(patient_dob, replacement_data.tags_to_fill["PatientBirthDate"])
        self.assertFalse("PatientBirthDate" in ds)
        fill_dcm.adjust_dicom_dataset(ds, replacement_data)
        self.assertTrue("PatientBirthDate" in ds)
        self.assertEqual(ds.PatientBirthDate, replacement_data.tags_to_fill["PatientBirthDate"])

    def test_several_missing_tags(self):
        """Input dataset does not contain required tags. All tags shall be filled and adjusted."""
        ds = self.load_dataset(DICOM_DATASET_JSON, tags_to_remove=["00080090", "00080012"])

        replacement_data = fill_dcm.update_data(parse_argument.InputTags({"InstanceCreationDate": None, "ReferringPhysicianName": None}, {}))
        fill_dcm.adjust_dicom_dataset(ds, replacement_data)

        self.assertEqual(
            replacement_data.tags_to_fill["InstanceCreationDate"],
            ds.InstanceCreationDate,
        )
        self.assertEqual(
            replacement_data.tags_to_fill["ReferringPhysicianName"],
            ds.ReferringPhysicianName,
        )

    def test_several_empty_tags(self):
        """Input dataset contains required tags, but are empty. All tags shall be adjusted."""
        ds = self.load_dataset(DICOM_DATASET_JSON, [])
        ds["InstanceCreationDate"].clear()
        ds["ReferringPhysicianName"].clear()

        self.assertEqual(ds["InstanceCreationDate"].VM, 0)
        self.assertEqual(ds["ReferringPhysicianName"].VM, 0)

        replacement_data = fill_dcm.update_data(parse_argument.InputTags({"InstanceCreationDate": None, "ReferringPhysicianName": None}, {}))
        fill_dcm.adjust_dicom_dataset(ds, replacement_data)

        self.assertEqual(
            replacement_data.tags_to_fill["InstanceCreationDate"],
            ds.InstanceCreationDate,
        )
        self.assertEqual(
            replacement_data.tags_to_fill["ReferringPhysicianName"],
            ds.ReferringPhysicianName,
        )

    def test_several_missing_tags_with_replacement_value(self):
        """Input dataset does not contain required tags. All tags shall be filled and adjusted with replacement value."""
        ds = self.load_dataset(DICOM_DATASET_JSON, tags_to_remove=["00080090", "00080012"])

        replacement_data = fill_dcm.update_data(
            parse_argument.InputTags(
                {
                    "InstanceCreationDate": "19980712",
                    "ReferringPhysicianName": "Zidane^Zinedine",
                },
                {},
            )
        )
        fill_dcm.adjust_dicom_dataset(ds, replacement_data)

        self.assertEqual(
            replacement_data.tags_to_fill["InstanceCreationDate"],
            ds.InstanceCreationDate,
        )
        self.assertEqual(
            replacement_data.tags_to_fill["ReferringPhysicianName"],
            ds.ReferringPhysicianName,
        )

    def test_several_missing_tags_with_values_to_replace(self):
        """Input dataset does not contain required tags. All tags shall be filled and adjusted with replacement value."""
        ds = self.load_dataset(DICOM_DATASET_JSON, tags_to_remove=["00080090", "00080012"])

        replacement_data = fill_dcm.update_data(
            parse_argument.InputTags(
                {},
                {
                    "InstanceCreationDate": "19980712",
                    "ReferringPhysicianName": "Zidane^Zinedine",
                },
            )
        )
        fill_dcm.adjust_dicom_dataset(ds, replacement_data)

        self.assertEqual(
            replacement_data.tags_to_replace["InstanceCreationDate"],
            ds.InstanceCreationDate,
        )
        self.assertEqual(
            replacement_data.tags_to_replace["ReferringPhysicianName"],
            ds.ReferringPhysicianName,
        )


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
