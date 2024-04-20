""" VR Generators: generate random data according to DICOM VR
"""

import string
from random import randrange, choices

PERSONAL_NAME_SAMPLE = {
    "first_names_male": ["James",
                         "Robert",
                         "John",
                         "Michael",
                         "David",
                         "William",
                         "Richard",
                         "Joseph",
                         "Thomas",
                         "Charles",
                         "Christopher",
                         "Daniel",
                         "Matthew",
                         "Anthony",
                         "Mark",
                         "Donald",
                         "Steven",
                         "Paul",
                         "Andrew",
                         "Joshua",
                         "Kenneth",
                         "Kevin",
                         "Brian",
                         "George",
                         "Timothy",
                         "Ronald",
                         "Edward",
                         "Jason",
                         "Jeffrey",
                         "Ryan",
                         "Jacob",
                         "Gary",
                         "Nicholas",
                         "Eric",
                         "Jonathan",
                         "Stephen",
                         "Larry",
                         "Justin",
                         "Scott",
                         "Brandon",
                         "Benjamin",
                         "Samuel",
                         "Gregory",
                         "Alexander",
                         "Frank",
                         "Patrick",
                         "Raymond",
                         "Jack",
                         "Dennis",
                         "Jerry",
                         "Tyler",
                         "Aaron",
                         "Jose",
                         "Adam",
                         "Nathan",
                         "Henry"],
    "first_names_female": ["Mary",
                           "Patricia",
                           "Jennifer",
                           "Linda",
                           "Elizabeth",
                           "Barbara",
                           "Susan",
                           "Jessica",
                           "Sarah",
                           "Karen",
                           "Lisa",
                           "Nancy",
                           "Betty",
                           "Margaret",
                           "Sandra",
                           "Ashley",
                           "Kimberly",
                           "Emily",
                           "Donna",
                           "Michelle",
                           "Carol",
                           "Amanda",
                           "Dorothy",
                           "Melissa",
                           "Deborah",
                           "Stephanie",
                           "Rebecca",
                           "Sharon",
                           "Laura",
                           "Cynthia",
                           "Kathleen",
                           "Amy",
                           "Angela",
                           "Shirley",
                           "Anna",
                           "Brenda",
                           "Pamela",
                           "Emma",
                           "Nicole",
                           "Helen",
                           "Samantha",
                           "Katherine",
                           "Christine",
                           "Debra",
                           "Rachel",
                           "Carolyn",
                           "Janet",
                           "Catherine",
                           "Maria",
                           "Heather",
                           "Diane",
                           "Ruth",
                           "Julie",
                           "Olivia",
                           "Joyce",
                           "Virginia"],
    "last_names": ["Smith",
                   "Johnson",
                   "Williams",
                   "Brown",
                   "Jones",
                   "Garcia",
                   "Miller",
                   "Davis",
                   "Rodriguez",
                   "Martinez",
                   "Hernandez",
                   "Lopez",
                   "Gonzalez",
                   "Wilson",
                   "Anderson",
                   "Thomas",
                   "Taylor",
                   "Moore",
                   "Jackson",
                   "Martin",
                   "Lee",
                   "Perez",
                   "Thompson",
                   "White",
                   "Harris",
                   "Sanchez",
                   "Clark",
                   "Ramirez",
                   "Lewis",
                   "Robinson",
                   "Walker",
                   "Young",
                   "Allen",
                   "King",
                   "Wright",
                   "Scott",
                   "Torres",
                   "Nguyen",
                   "Hill",
                   "Flores",
                   "Green",
                   "Adams",
                   "Nelson",
                   "Baker",
                   "Hall",
                   "Rivera",
                   "Campbell",
                   "Mitchell",
                   "Carter",
                   "Roberts"]
}


def generate_id() -> str:
    """ Generate a Patient ID following DICOM LO VR spec
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Patient ID is generated as: XXYYYY where X is a
    Returns:
        A Patient ID as a string
    """
    return "".join(choices(string.ascii_uppercase + string.digits, k=10))


def generate_age_string() -> str:
    """Generate an Age String and follows DICOM AS VR spec.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Only ages in years are generated: "XXXY" where 'X' are digits characters

    Returns:
        A DICOM Age String
    """
    return "".join(choices(string.digits, k=3)+["Y"])


def generate_decimal_string() -> str:
    """Generate a Decimal String and follows DICOM DS VR spec.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Only fixed point numbers are generating: only digits from 1 to 16 bytes

    Returns:
        A DICOM Decimal String
    """
    return "".join(choices(string.digits, k=randrange(1, 16)))


def generate_date_time() -> str:
    """Generate a Date Time and follows DICOM DT VR spec.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Only the following fields from DT are filled: YYYYMMDDHHMMSS

    Returns:
        A DICOM Date Time
    """
    return f"{generate_date()}{randrange(0, 23):02}{randrange(0, 59):02}{randrange(0, 59):02}"


def generate_integer_string() -> str:
    """ Generate a Integer String and follows DICOM IS VR spec.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Generate Integer in the range -2^31 <= n <= 2^31-1

    Returns:
        str: Integer string
    """
    return f"{randrange(-1*2**31, (2**31)-1)}"


def generate_personal_name() -> str:
    """ Generate a personal name and follow DICOM PN VR spec.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Only first and last names are filled.

    Returns:
        A DICOM personal name
    """
    possible_first_names = []
    possible_first_names.extend(PERSONAL_NAME_SAMPLE["first_names_female"])
    possible_first_names.extend(PERSONAL_NAME_SAMPLE["first_names_male"])
    return f"{choices(PERSONAL_NAME_SAMPLE['last_names'])[0]}^{choices(possible_first_names)[0]}"


def generate_date() -> str:
    """ Generate a data and follow DICOM DA VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    Years are in range [1950, 2020]
        Returns:
            A DICOM date
        """
    return f"{randrange(1950, 2020)}{randrange(1, 12):02}{randrange(1, 30):02}"


def generate_lo() -> str:
    """ Generate a data and follow DICOM LO VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
        Returns:
            A randomized LO value with at least one character and max 64
    """
    return "".join(choices(string.ascii_letters + string.digits, k=randrange(1, 64)))


def generate_long_text() -> str:
    """ Generate a data and follow DICOM LT VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
        Returns:
            A randomized LT value with at least one character and max 1024
    """
    return "".join(choices(string.ascii_letters + string.digits, k=randrange(1, 1024)))


def generate_short_string() -> str:
    """ Generate a data and follow DICOM SH VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
        Returns:
            A randomized SH value with at least one character and max 16
    """
    return "".join(choices(string.ascii_letters + string.digits, k=randrange(1, 16)))


def generate_short_text() -> str:
    """ Generate a data and follow DICOM ST VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
        Returns:
            A randomized ST value with at least one character and max 1024
    """
    return "".join(choices(string.ascii_letters + string.digits, k=randrange(1, 1024)))


def generate_time() -> str:
    """ Generate a data and follow DICOM TM VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
        Returns:
            A randomized TM value with the format "HHMMSS"
    """
    return f"{randrange(0, 23):02}{randrange(0, 59):02}{randrange(0, 59):02}"


def generate_unique_identifier() -> str:
    """ Generate a data and follow DICOM UI VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
        Returns:
            A randomized UI value with the format <digits>.<digits>.<digits>.<digits>
    """
    return f"{randrange(1,1000)}.{randrange(1,1000)}.{randrange(1,1000)}.{randrange(1,1000)}"


def generate_unsigned_short() -> int:
    """ Generate a data and follow DICOM US VR specs.
    https://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
        Returns:
            A randomized US, a number in the range 0 <= x < 65536
    """
    return randrange(0, 65536)
