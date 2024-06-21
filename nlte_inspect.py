import requests
import re
import csv

"""
The code takes in values for the field parameters one-by-one from a file and then uses these fields to post an html request to the inspect-stars website and get the values
by parsing the result for the second_last value if it is between -1 and 1. If there are changes made to the limits, wavelengths we can run for, or the format of output 
on the website, the code will have to be updated.

The elements done: Fe I (26), Na (11), O (8), Li (3), Sr (38) [RUN SEPARATELY]

Make sure the required libraries [requests, re, csv] are installed, otherwise first use pip on command line to install them 

website: http://inspect-stars.com/index.php?n=Main.HomePage

Last updated: July 21, 2023 (sanilm@umich.edu)
"""

# initial values to be updated to run the code
element = "Na"   # Fe, O, Li, Sr or Na, for other elements, will have to add html_snippet for their wav values using source code and their limits

# Corr is the Delta value, Corrected is delta value + abundance value
output_file = "nlte_fe1ona.csv"  # output with these headers: ["Name", "ID", "Wav", "EqW", "Abundance", "Corr", "Corrected"] # ID must be number, for eg 26 for Fe I

# input 1 needed with these headers in this order: ["Name","ID","Wav","EqW","Abundance","Corr","Corrected"] the individual headings do not matter but the order does
file1 = "nlte_fe1o.csv"  # lines from this file are copied as is in case of no match or ID other than the one entered

# input 2 needed with these headers in this order: ["Name","Teff","Logg","FeH","Vt","ID","Wav","EqW","Abundance"]
file2 = "output_nlte_new.csv"  # used to get the parameters for each line

# FOR THE ROWS THAT ARE PRINTED WHILE THE CODE RUNS, NEED TO RUN MANUALLY TO GET CLOSEST POINT ON THE GRID

# Not need to change the code below this line unless need to update the code
########################################################################################
########################################################################################
########################################################################################

def get_nearest_option(input_value, html_snippet):
    # Extract the option values from the HTML snippet using regular expressions
    # option_values = re.findall(r'<option value="(.*)">.*</option>', html_snippet)
    wav_values = re.findall(r'<option value=".*">(.*)</option>', html_snippet)

    # Convert the option values to floats
    # option_values = [float(value) for value in option_values if isinstance(value, str) for value in [value] if value and value.strip()]
    wav_values = [float(value) for value in wav_values if isinstance(value, str) for value in [value] if
                  value and value.strip()]

    # Find the nearest option value to the input value
    nearest_value = min(wav_values, key=lambda x: abs(x - input_value))

    # Check if the nearest value is within the range
    if abs(nearest_value - input_value) > 0.199:
        return None

    # Find the index of the nearest value
    index = wav_values.index(nearest_value)

    # Return the option value and index
    return nearest_value, index

def process_input_values(element, equivalent_width, temperature, metallicity, log_gravity, microturbulence, wavelength_index):
    # uses field values to process a get request to the website, may need to change the url
    # Prepare the URL with the parameters
    url = 'http://www.inspect-stars.com/cp/application.py/A_from_e'
    if element == "Fe":
        params = {
            'element_name': 'Fe',
            'e': equivalent_width,
            't': temperature,
            'g': log_gravity,
            'x': microturbulence,
            'wi': wavelength_index
        }
    elif element == "Na":
        params = {
            'element_name': 'Na',
            'e': equivalent_width,
            't': temperature,
            'g': log_gravity,
            'f': metallicity,
            'x': microturbulence,
            'wi': wavelength_index
        }
    elif element == "O":
        params = {
            'element_name': 'O',
            'e': equivalent_width,
            't': temperature,
            'g': log_gravity,
            'f': metallicity,
            'x': microturbulence,
            'wi': wavelength_index
        }
    elif element == "Li":
        params = {
            'element_name': 'Li',
            'e': equivalent_width,
            't': temperature,
            'g': log_gravity,
            'f': metallicity,
            'x': microturbulence,
            'wi': wavelength_index
        }
    elif element == "Sr":
        params = {
            'element_name': 'Sr',
            'e': equivalent_width,
            't': temperature,
            'g': log_gravity,
            'f': metallicity,
            'x': microturbulence,
            'wi': wavelength_index
        }
    # Send a GET request with the parameters
    response = requests.get(url, params=params)

    # Extract the relevant data from the response using regular expressions
    pattern = r'.*<pre>(.*?)<\/pre>'
    matches = re.findall(pattern, response.text, re.DOTALL)

    if matches:
        numbers = re.findall(r'[-+]?\d+\.\d+', matches[0])
        if len(numbers) >= 2:
            return numbers[-2]

    return None

if element == "Fe":
# Extract the option values from the HTML snippet and define limits
    id_num = "26"
    vt_min = 1.0
    vt_max = 2.0
    logg_min = 1.0
    logg_max = 5.0
    k_min = 4000.0
    k_max = 8000.0
    ew_min = 1.0
    ew_max = 5000.0
    feh_min = -5.0
    feh_max = 0.5
    html_snippet = """
<option value="0">3440.610</option>
<option value="1">3440.990</option>
<option value="2">3465.860</option>
<option value="3">3475.440</option>
<option value="4">3490.570</option>
<option value="5">3565.380</option>
<option value="6">3570.100</option>
<option value="7">3581.190</option>
<option value="8">3608.860</option>
<option value="9">3618.770</option>
<option value="10">3719.920</option>
<option value="11">3737.120</option>
<option value="12">3727.620</option>
<option value="13">3745.560</option>
<option value="14">3748.260</option>
<option value="15">3758.230</option>
<option value="16">3763.790</option>
<option value="17">3815.840</option>
<option value="18">3820.430</option>
<option value="19">3824.440</option>
<option value="20">3825.870</option>
<option value="21">3840.440</option>
<option value="22">3856.370</option>
<option value="23">3859.910</option>
<option value="24">3922.910</option>
<option value="25">4045.810</option>
<option value="26">4063.590</option>
<option value="27">4071.740</option>
<option value="28">4235.940</option>
<option value="29">4250.120</option>
<option value="30">4250.790</option>
<option value="31">4415.120</option>
<option value="32">4445.470</option>
<option value="33">4494.560</option>
<option value="34">4920.500</option>
<option value="35">4994.130</option>
<option value="36">5044.210</option>
<option value="37">5198.700</option>
<option value="38">5216.270</option>
<option value="39">5225.520</option>
<option value="40">5232.940</option>
<option value="41">5236.200</option>
<option value="42">5242.490</option>
<option value="43">5247.040</option>
<option value="44">5250.210</option>
<option value="45">5269.540</option>
<option value="46">5281.790</option>
<option value="47">5379.570</option>
<option value="48">5383.370</option>
<option value="49">5434.521</option>
<option value="50">5491.830</option>
<option value="51">5586.750</option>
<option value="52">5600.220</option>
<option value="53">5661.350</option>
<option value="54">5662.520</option>
<option value="55">5696.090</option>
<option value="56">5701.540</option>
<option value="57">5705.460</option>
<option value="58">5778.450</option>
<option value="59">5784.660</option>
<option value="60">5855.080</option>
<option value="61">5916.250</option>
<option value="62">5956.690</option>
<option value="63">6065.479</option>
<option value="64">6082.710</option>
<option value="65">6151.620</option>
<option value="66">6173.330</option>
<option value="67">6200.310</option>
<option value="68">6219.280</option>
<option value="69">6240.650</option>
<option value="70">6252.560</option>
<option value="71">6265.130</option>
<option value="72">6297.790</option>
<option value="73">6311.500</option>
<option value="74">6430.850</option>
<option value="75">6498.940</option>
<option value="76">6518.370</option>
<option value="77">6574.229</option>
<option value="78">6593.870</option>
<option value="79">6609.110</option>
<option value="80">6699.140</option>
<option value="81">6726.670</option>
<option value="82">6739.521</option>
<option value="83">6750.150</option>
<option value="84">6793.260</option>
<option value="85">6810.260</option>
<option value="86">6837.010</option>
<option value="87">6854.820</option>
<option value="88">6945.200</option>
<option value="89">6978.850</option>
<option value="90">7401.680</option>
<option value="91">7912.870</option>
<option value="92">8293.500</option>
<option value="93">4233.170</option>
<option value="94">4491.390</option>
<option value="95">4508.290</option>
<option value="96">4576.330</option>
<option value="97">4582.840</option>
<option value="98">4583.830</option>
<option value="99">4620.520</option>
<option value="100">4923.930</option>
<option value="101">5018.440</option>
<option value="102">5169.020</option>
<option value="103">5197.580</option>
<option value="104">5234.620</option>
<option value="105">5264.810</option>
<option value="106">5284.110</option>
<option value="107">5325.550</option>
<option value="108">5414.070</option>
<option value="109">5425.260</option>
<option value="110">6239.950</option>
<option value="111">6247.560</option>
<option value="112">6369.460</option>
<option value="113">6432.680</option>
<option value="114">6456.380</option>
<option value="115">6516.080</option>
<option value="116">7222.390</option>
<option value="117">7224.490</option>
<option value="118">7515.830</option>
<option value="119">7711.720</option>
</select>
</td><td></td></tr>
"""
elif element == "Na":
    id_num = "11"
    vt_min = 1.0
    vt_max = 5.0
    logg_min = 0.0
    logg_max = 5.0
    k_min = 3800.0
    k_max = 8000.0
    ew_min = 1.0
    ew_max = 5000.0
    feh_min = -5.0
    feh_max = 0.5
    html_snippet = """
<option value="0">4751.820</option>
<option value="1">5148.830</option>
<option value="2">5682.630</option>
<option value="3">5688.200</option>
<option value="4">5889.950</option>
<option value="5">5895.920</option>
<option value="6">6154.220</option>
<option value="7">6160.740</option>
<option value="8">8183.250</option>
<option value="9">8194.800</option>
<option value="10">10746.440</option>
"""
elif element == "O":
    id_num = "8"
    vt_min = 0.5
    vt_max = 2.0
    logg_min = 3.0
    logg_max = 5.0
    k_min = 5000.0
    k_max = 6500.0
    ew_min = 1.0
    ew_max = 5000.0
    feh_min = -3.0
    feh_max = 0.0
    html_snippet = """
<option value="0">6158.193</option>
<option value="1">6300.255</option>
<option value="2">6363.838</option>
<option value="3">7771.957</option>
<option value="4">7774.156</option>
<option value="5">7775.356</option>
"""
elif element == "Li":
    id_num = "3"
    vt_min = 1.0
    vt_max = 5.0
    logg_min = 1.0
    logg_max = 5.0
    k_min = 4000.0
    k_max = 8000.0
    ew_min = 1.0
    ew_max = 5000.0
    feh_min = -5.0
    feh_max = 0.5
    html_snippet = """
<option value="0">6103.600</option>
<option value="1">6707.810</option>
"""
elif element == "Sr":
    id_num = "38"
    vt_min = 1.0
    vt_max = 1.0
    logg_min = 2.2
    logg_max = 4.6
    k_min = 4400.0
    k_max = 6400.0
    ew_min = 1.0
    ew_max = 5000.0
    feh_min = -3.9
    feh_max = 0.0
    html_snippet = """
<option value="0">4077.710</option>
<option value="1">4215.520</option>
<option value="2">10036.660</option>
<option value="3">10327.310</option>
<option value="4">10914.880</option>
"""
num = None
corr = []
err= 0
with open(output_file, "w", newline="") as newfile:
    writer = csv.writer(newfile)
    writer.writerow(["Name", "ID", "Wav", "EqW", "Abundance", "Corr", "Corrected"])
    with open(file1, "r") as file:
        next(file)
        read2 = csv.reader(file, delimiter=",")
        lines = list(read2)
        with open(file2, "r") as f:
            next(f)
            read = csv.reader(f, delimiter=",")
            num_rows = 0
            for row in read:
                num_rows += 1

                # Define the field values, may have to change the values depending on the file structure
                name = row[0]
                equivalent_width = float(row[-2])
                temperature = float(row[1])
                log_gravity = float(row[2])
                metallicity = float(row[3])
                microturbulence = float(row[4])

                id = row[5]
                input_value = float(row[6])  # Input value for comparison
                abun = float(row[-1])
                if id == id_num:
                    # error checking and choosing nearest value for the list
                    if microturbulence < vt_min:
                        microturbulence = vt_min
                    elif microturbulence > vt_max:
                        microturbulence = vt_max
                    if log_gravity < logg_min:
                        log_gravity = logg_min
                    elif log_gravity > logg_max:
                        log_gravity = logg_max
                    if temperature < k_min:
                        temperature = k_min
                    elif temperature > k_max:
                        temperature = k_max
                    if metallicity < feh_min:
                        metallicity = feh_min
                    elif metallicity > feh_max:
                        metallicity = feh_max
                    if equivalent_width < ew_min:
                        equivalent_width = ew_min
                    elif equivalent_width > ew_max:
                        equivalent_width = ew_max

                    nearest_option = get_nearest_option(input_value, html_snippet)  # html_snippet for the element
                    if nearest_option is None:
                        corr.append(0)
                        writer.writerow([name, id, input_value, equivalent_width, abun, "", ""])  # if no wavelength within 0.199, returns the line as is
                        continue

                    nearest_value, index = nearest_option
                    num = process_input_values(element, equivalent_width, temperature, metallicity, log_gravity, microturbulence, index)
                    # print(num)
                    if num == None or (float(num) >= 1. or float(num) <= -1.):
                        corr.append(0)
                        writer.writerow([name, id, input_value, equivalent_width, abun, "", ""])  # an error, may have to manually check to find the closest value on grid
                        print(f"Name: {name}, Element ID: {id}, EW: {equivalent_width}, Teff: {temperature}, Logg: {log_gravity}, Feh: {metallicity}, Vt: {microturbulence}, Nearest Wav: {input_value}")
                        err +=1
                        continue
                    else:
                        corr.append(1)
                        writer.writerow([name, id, input_value, equivalent_width, abun, num, abun+float(num)])   # correctly run
                else:
                    corr.append(0)
                    writer.writerow(lines[num_rows-1])  # element id not there, so just copies the row as is

print(f"Errors {err}, rows {num_rows}, length of corr {len(corr)}")