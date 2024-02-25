# Introduction

FillDCM is the DICOM tool you need if you have to:
- fill empty or missing DICOM tags with random or specified values
- overwrite some DICOM tags with a specified values

```sh
> python fill_dcm.py --help
usage: FillDCM [-h] [-t --tag] [-to --tag-overwrite] [-ov] dcm_file [dcm_file ...]

Tool to fill empty DICOM tags or to overwrite others.

positional arguments:
    dcm_file             DICOM files to edit

options:
    -h, --help           show this help message and exit
    -t --tag             DICOM tag to fill if value is empty or undefined
    -to --tag-overwrite  DICOM tag to overwrite with the specified value
    -ov, --overwrite     Overwrite the original file. By default "_generated" is appended the the original filename and a new file is created.
```
