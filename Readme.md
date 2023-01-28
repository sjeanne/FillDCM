# Introduction

The DICOM standard already defines header tags with their VM and VR. But some projects may need additionnal and stricter rules. DCMAdjust's goal is to edit DICOM files to make them match some particular requirements.

-   0010,0010 - Patient name (PN): not null and not empty
-   XXXX,XXXX - Patient's birtdate: not null and not empty
-   XXXX,XXXX - Patient's ID: not null and not empty
-   XXXX,XXXX - Refering Physician (PN): not null and not empty
-   XXXX,XXXX - Device Serial Number: not null and not empty
