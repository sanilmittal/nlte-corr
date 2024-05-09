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
requests, re, csv, selenium

Download the Python files.

Usage for nlte_inspect.py
-----
Input file:

Output file: 

O I, Na I, Fe 

Change the input and output file names, and run!

Usage for nlte_mpia.py
-----
Input file:

Output file: 

Mg I, Si I, Fe II 

Change the input and output file names, and run!
