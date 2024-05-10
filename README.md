NLTE Corrections
--------
We provide codes to calculate NLTE corrections from two websites: INSPECT-STARS (http://inspect-stars.com/index.php?n=Main.HomePage) and NLTE MPIA (https://nlte.mpia.de/gui-siuAC_secE.php)

The code currently supports NLTE corrections for the following elements: 

* O I, Na I, Fe I (INSPECT-STARS)
* Mg I, Si I, Fe II (NLTE MPIA)

Authors
-------
 - Sanil Mittal (University of Michigan)
 - Ian U. Roederer (North Carolina State University)

Installation
------------
Required packages to install for INSPECT-STARS (nlte_inspect.py):
requests, re, csv

Required packages to install for NLTE MPIA (nlte_mpia.py):
re, csv, selenium

They can be installed using pip.

Download the Python files.

Usage for nlte_inspect.py
-----

The code takes in values for the field parameters one-by-one from a file and then uses these fields to post an html request to the inspect-stars website and get the values
by parsing the result for the second_last value if it is between -1 and 1. If there are changes made to the limits, wavelengths we can run for, or the format of output 
on the website, the code will have to be updated.

Input file 1: 

Values of the file need to be in this order: ["Star Name","ID","Wav","EqW","Abundance","Correction","Corrected Value"] 

The individual headings do not matter but the order does. Lines from this file are copied as is, in case of no match or ID other than the one entered.

Input file 2:

Values of the file need to be in this order: ["Star Name","Effective Temperature","Logg","[Fe/H]","Microturbulence","ID","Wavelength","EqW","Abundance"]

This file is used to get the parameters for each line to calculate the corrections.

Output file: 

Value of the file will be in this order: ["Star Name", "ID", "Wavelength", "EqW", "Abundance", "Correction", "Corrected"]

Here, Correction is the Delta value, and Corrected is the delta value + abundance value, hence the NLTE-corrected abundance value

Supported elements: O I, Na I, Fe I

Change the input and output file names, and run!

Usage for nlte_mpia.py
-----
The code takes in values for the field parameters one star at a time from a file and then uses these fields to post an html request to the NLTE website and get the values
by parsing the result for the delta value. If there are changes made to the limits, wavelengths we can run for, or the format of output 
on the website, the code will have to be updated.

Website value range: if correction: -1,..,1 OK; 0.000 no NLTE departures for this line; 
30 line too weak (EW < 1mA) or line is not in linelist;
20 NLTE not converged; 
10 error in lineformation

Will need to manually check for 10, 20 , 30-- 30 most common, just delete those Correction values

Input file 1: 

Values of the file need to be in this order: ["Star Name","ID","Wav","EqW","Abundance","Correction","Corrected Value"] 

The individual headings do not matter but the order does. Lines from this file are copied as is, in case of no match or ID other than the one entered.

Input file 2:

Values of the file need to be in this order: ["Star Name","Effective Temperature","Logg","[Fe/H]","Microturbulence"]

This file is used to get the parameters for each line to calculate the corrections.

Output file: 

Value of the file will be in this order: ["Star Name", "ID", "Wavelength", "EqW", "Abundance", "Correction", "Corrected"]

Here, Correction is the Delta value, and Corrected is the delta value + abundance value, hence the NLTE-corrected abundance value

Supported elements: Mg I, Si I, Fe II 

Change the input and output file names, and run!

Citation
-----
If the code was helpful, please cite:

Mittal and Roederer (2024), in prep

For INSPECT-STARS:

- O I:
- Na I:
- Fe I:

For NLTE MPIA:

- Mg I:
- Si I:
- Fe II:
