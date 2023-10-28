import unittest
from fill_dcm import generate_personal_name, generate_date, generate_id, generate_data, Gender


class TestGenerates(unittest.TestCase):
    def test_generate_data(self):
        """ Default call to generate_date: no gender, no input values
        """
        generated_data = generate_data()
        self.assertTrue('PatientName' in generated_data)
        self.assertTrue('ReferringPhysicianName' in generated_data)
        self.assertTrue('PatientBirthDate' in generated_data)
        self.assertTrue('PatientSex' in generated_data)
        self.assertTrue('PatientID' in generated_data)
        self.assertTrue('DeviceSerialNumber' in generated_data)

    def test_generate_data_valid_genders(self):
        """  Call generate_data() with different valid gender values
        """
        for gender_value in Gender:
            generated_data = generate_data(
                patient_sex_from_dcm=gender_value.value)
            self.assertTrue('PatientName' in generated_data)
            self.assertEqual(generated_data["PatientSex"], gender_value.value)

    def test_generate_data_invalid_genders(self):
        """ Call generate_data() with invalid gender values
        """
        for invalid_gender in ["", "Invalid", "MALE", "Cat"]:
            generated_data = generate_data(patient_sex_from_dcm=invalid_gender)
            self.assertTrue('PatientName' in generated_data)
            self.assertEqual(
                generated_data["PatientSex"], Gender.NOT_SPECIFIED.value)

    def test_generate_data_values(self):
        """ Call to generate_data() with input values. Generated data shall match input values
        """
        input_values = {
            "PatientName": "patient^name^complicated",
            "PatientID": "1234567890AZERTY",
            "PatientBirthDate": "20000101",
            "PatientSex": "F",
            "ReferringPhysicianName": "Dr^Ref^Phy",
            "DeviceSerialNumber": "AT40",
        }

        generated_data = generate_data(input_values)

        self.assertEqual(
            generated_data["PatientName"], input_values["PatientName"])
        self.assertEqual(
            generated_data["PatientID"], input_values["PatientID"])
        self.assertEqual(
            generated_data["PatientBirthDate"], input_values["PatientBirthDate"])
        self.assertEqual(
            generated_data["ReferringPhysicianName"], input_values["ReferringPhysicianName"])
        self.assertEqual(
            generated_data["DeviceSerialNumber"], input_values["DeviceSerialNumber"])

    def test_generate_personal_name(self):
        pn = generate_personal_name()
        splitted_pn = pn.split('^')
        self.assertEqual(len(splitted_pn), 2)
        self.assertGreater(len(splitted_pn[0]), 0)
        self.assertGreater(len(splitted_pn[1]), 0)

    def test_generate_date(self):
        date = generate_date()
        self.assertEqual(len(date), 8)
        self.assertTrue(date.isdigit())

    def test_generate_patient_id(self):
        patient_id = generate_id()
        self.assertGreater(len(patient_id), 0)
