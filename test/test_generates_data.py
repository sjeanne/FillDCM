import unittest
from fill_dcm import generate_personal_name, generate_date, generate_data


class TestGenerates(unittest.TestCase):
    def test_generate_data(self):
        generated_data = generate_data()
        self.assertTrue('PatientName' in generated_data)
        self.assertTrue('ReferingPhysician' in generated_data)
        self.assertTrue('PatientBirthDate' in generated_data)

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
