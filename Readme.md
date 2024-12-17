# Introduction

FillDCM is the DICOM tool you need if you have to:
- fill empty or missing DICOM tags with random or specified values
- replace some DICOM tags with a specified values

Tags are specified by their names as string, following DICOM dictionary: PatientID, AcquisitionData, etc.

```sh
> python filldcm --help
usage: FillDCM [-h] [-f --fill-tag] [-r --replace-tag] [-j --json] [-ov] dcm_file [dcm_file ...]

Tool to fill missing or empty DICOM tags or to replace others.

positional arguments:
  dcm_file              List of DICOM files to edit

options:
  -h, --help            show this help message and exit
  -f --fill-tag         DICOM tag to fill if missing or if its value is empty or undefined. A value to fill can be specified. Tag specification: <Tag name as a string>[=<value>]
  -r --replace-tag      DICOM tag to replace with the specified value. If the tag doesn't exist, it is appended to the dataset. Tags specification: <Tag name as a string>=<value>
  -j --json             Specify a JSON file as input. This JSON file has a list of tags to fill or to replace.
  -ov, --overwrite-file Overwrite the original file. By default "_generated" is appended the the original filename and a new file is created.
```

# Examples

## Fill a list of empty/missing tags

You want patient's data to not be empty or missing and don't expect a particular value:
```sh
> python filldcm.py 
    --fill-tag PatientName 
    --fill-tag PatientID 
    --fill-tag PatientBirthDate 
    --fill-tag PatientSex
    --fill-tag PatientWeight 
    <list of dcm files>

```

## Overwrite some particular tags

You want to overwrite all tags related to the Institution
```sh
> python filldcm.py 
    --replace-tag InstitutionName="Github Hospital" 
    --replace-tag InstitutionAddress="42 Git street, Github town" 
    <list of dcm files>

```

