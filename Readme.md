# Introduction

The DICOM standard already defines header tags with their VM and VR. But some projects may need additionnal and stricter rules. DCMAdjust's goal is to edit DICOM files to make them match some particular requirements.

-   0008,0090 - Referring Physician (PN): not null and not empty
-   0010,0010 - Patient name (PN): not null and not empty
-   0010,0020 - Patient's ID: not null and not empty
-   0010,0030 - Patient's birth date: not null and not empty
-   0018,1000 - Device Serial Number
