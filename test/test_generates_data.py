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
        self.assertTrue('PatientID' in generated_data)
        self.assertTrue('DeviceSerialNumber' in generated_data)

    def test_generate_data_genders(self):
        """  Call generate_data() with different gender values
        """
        for gender_value in Gender:
            generated_data = generate_data(patient_gender=gender_value)
            self.assertTrue('PatientName' in generated_data)

    def test_generate_data_values(self):
        """ Call to generate_data() with input values. Generated data shall match input values
        """
        input_values = {
            "patient_name": "patient^name^complicated",
            "patient_id": "1234567890AZERTY",
            "patient_birthdate": "20000101",
            "referring_physician_name": "Dr^Ref^Phy",
            "device_serial_number": "AT40",
        }

        generated_data = generate_data(input_values)

        self.assertEqual(
            generated_data["PatientName"], input_values["patient_name"])
        self.assertEqual(
            generated_data["PatientID"], input_values["patient_id"])
        self.assertEqual(
            generated_data["PatientBirthDate"], input_values["patient_birthdate"])
        self.assertEqual(
            generated_data["ReferringPhysicianName"], input_values["referring_physician_name"])
        self.assertEqual(
            generated_data["DeviceSerialNumber"], input_values["device_serial_number"])

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
