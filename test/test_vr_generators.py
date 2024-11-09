""" DVR Generators unit tests
"""

import string
import unittest

from filldcm import fill_dcm


class TestVRGenerators(unittest.TestCase):
    """Test all VR Generators"""

    def test_generate_personal_name(self):
        """Test generate_personal_name()"""
        pn = fill_dcm.vr_generators.generate_personal_name()
        splitted_pn = pn.split("^")
        self.assertEqual(len(splitted_pn), 2)
        self.assertGreater(len(splitted_pn[0]), 0)
        self.assertGreater(len(splitted_pn[1]), 0)

    def test_generate_date(self):
        """Test generate_date()"""
        date = fill_dcm.vr_generators.generate_date()
        self.assertEqual(len(date), 8)
        self.assertTrue(date.isdigit())
        # Check years
        self.assertLessEqual(int(date[0:4]), 2020)
        # Check months
        self.assertLessEqual(int(date[4:6]), 12)
        # Check days
        self.assertLessEqual(int(date[6:]), 31)

    def test_generate_patient_id(self):
        """Test generate_patient_id()"""
        patient_id = fill_dcm.vr_generators.generate_id()
        self.assertGreater(len(patient_id), 0)

    def test_generate_lo(self):
        """Test generate_lo()"""
        long_string = fill_dcm.vr_generators.generate_lo()
        self.assertLessEqual(len(long_string), 64)
        self.assertGreaterEqual(len(long_string), 1)

    def test_generate_age_string(self):
        """Test generate_age_string()"""
        age_string = fill_dcm.vr_generators.generate_age_string()
        self.assertEqual(len(age_string), 4)
        self.assertTrue(age_string[0:3].isdigit())
        self.assertEqual(age_string[-1], "Y")

    def test_generate_decimal_string(self):
        """Test generate_decimal_string()"""
        decimal_string = fill_dcm.vr_generators.generate_decimal_string()
        self.assertNotEqual(len(decimal_string), 0)
        self.assertLessEqual(len(decimal_string), 16)
        for c in list(decimal_string):
            self.assertIn(c, string.digits)

    def test_generate_date_time(self):
        """Test generate_date_time()"""
        date_time = fill_dcm.vr_generators.generate_date_time()
        self.assertEqual(len(date_time), 14)
        self.assertTrue(date_time.isdigit())
        # Check years
        self.assertLessEqual(int(date_time[0:4]), 2020)
        # Check months
        self.assertLessEqual(int(date_time[4:6]), 12)
        # Check days
        self.assertLessEqual(int(date_time[6:8]), 31)
        # Check hours
        self.assertLessEqual(int(date_time[8:10]), 23)
        # Check minutes
        self.assertLessEqual(int(date_time[10:12]), 59)
        # Check seconds
        self.assertLessEqual(int(date_time[12:]), 59)

    def test_generate_integer_string(self):
        """Test generate_integer_string()"""
        integer_string = fill_dcm.vr_generators.generate_integer_string()
        integer = int(integer_string)
        self.assertGreaterEqual(integer, -1 * 2**31)
        self.assertLessEqual(integer, (2**31) - 1)

    def test_generate_long_text(self):
        """Test generate_long_text()"""
        long_text = fill_dcm.vr_generators.generate_long_text()
        self.assertLessEqual(len(long_text), 1024)
        self.assertGreaterEqual(len(long_text), 1)

    def test_generate_short_string(self):
        """Test generate_short_string()"""
        short_string = fill_dcm.vr_generators.generate_short_string()
        self.assertLessEqual(len(short_string), 16)
        self.assertGreaterEqual(len(short_string), 1)

    def test_generate_short_text(self):
        """Test generate_short_text()"""
        short_text = fill_dcm.vr_generators.generate_short_text()
        self.assertLessEqual(len(short_text), 1024)
        self.assertGreaterEqual(len(short_text), 1)

    def test_generate_time(self):
        """Test generate_time()"""
        time = fill_dcm.vr_generators.generate_time()
        self.assertEqual(len(time), 6)
        self.assertTrue(time.isdigit())
        # Check hours
        self.assertLessEqual(int(time[0:2]), 23)
        # Check minutes
        self.assertLessEqual(int(time[2:4]), 59)
        # Check seconds
        self.assertLessEqual(int(time[4:]), 59)

    def test_generate_unique_identifier(self):
        """Test generate_unique_identifier()"""
        unique_identifier = fill_dcm.vr_generators.generate_unique_identifier()
        self.assertLessEqual(len(unique_identifier), 64)
        splitted_uid = unique_identifier.split(".")
        self.assertEqual(len(splitted_uid), 4)
        for part in splitted_uid:
            int(part)  # each part is a number

    def test_generate_unsigned_short(self):
        """Test generate_unsigned_short()"""
        unsigned_short = fill_dcm.vr_generators.generate_unsigned_short()
        self.assertGreaterEqual(unsigned_short, 0)
        self.assertLess(unsigned_short, 65536)
