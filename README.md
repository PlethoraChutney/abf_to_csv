# ABF to CSV
Convert ABF files to CSV for use with external plotting
and analysis. A wrapper around the excellent
[pyABF](https://github.com/swharden/pyABF) by Scott Harden.

## Installation
`python3 -m pip install -r requirements.txt`

## Usage
Run the script with an input glob (something like "*.abf" or "data/*.abf").
Optionally you can tell it which channels correspond to Voltage, Current, or Barrel.
The Baconguis Lab defaults are set.