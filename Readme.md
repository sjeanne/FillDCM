# Introduction

FillDCM is the DICOM tool you need if you have to:
- fill empty or missing DICOM tags with random or specified values
- overwrite some DICOM tags with a specified values

Tags are specified by their names as string, following DICOM dictionary: PatientID, AcquisitionData, etc.

```sh
> python fill_dcm.py --help
usage: FillDCM [-h] [-t --tag] [-to --tag-overwrite] [-ov] dcm_file [dcm_file ...]

Tool to fill empty or missing DICOM tags or to overwrite others.

positional arguments:
    dcm_file             DICOM files to edit

options:
    -h, --help           show this help message and exit
    -t --tag             DICOM tag to fill if value is empty or missing. Tags are formatted: <Tag name as a string>[=<value>]
    -to --tag-overwrite  DICOM tag to overwrite with the specified value. Tags are formatted: <Tag name as a string>=<value>
    -ov, --overwrite     Overwrite the original file. By default "_generated" is appended the the original filename and a new file is created.
```

# Examples

## Fill a list of empty/missing tags

You want patient's data to not be empty or missing and don't expect a particular value:
```sh
> python fill_dcm.py --tag PatientName --tag PatientID --tag PatientBirthDate --tag PatientSex --tag PatientWeight <list of dcm files>

```

## Overwrite some particular tags

You want to overwrite all tags related to the Institution
```sh
> python fill_dcm.py --tag-overwrite InstitutionName="Github Hospital" --tag-overwrite InstitutionAddress="42 Git street, Github town" <list of dcm files>

```

