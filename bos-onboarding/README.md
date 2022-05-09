# BOS Automation Tools
...

## Installation

### Pre-requisites

```
python3 -m pip install -r requirements.txt
```

## Excel sheet template

[`test/test_sheet.xlsx`](test/test_sheet.xlsx)

## Convert an Excel spreadsheet to a UDMI site model

```
./sheet2udmi.py -h
     _               _   ____  _   _ ____  __  __ ___ 
 ___| |__   ___  ___| |_|___ \| | | |  _ \|  \/  |_ _|
/ __| '_ \ / _ \/ _ \ __| __) | | | | | | | |\/| || | 
\__ \ | | |  __/  __/ |_ / __/| |_| | |_| | |  | || | 
|___/_| |_|\___|\___|\__|_____|\___/|____/|_|  |_|___|
                                                      

usage: sheet2udmi.py [-h] [-v] [-d] [-i INPUT] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase the verbosity level
  -d, --debug           print debug information
  -i INPUT, --input INPUT
                        input Excel sheet file name
  -o OUTPUT, --output OUTPUT
                        output folder name
```

## Convert an Excel spreadsheet to a DBO building config file

```
./sheet2dbo.py -h
     _               _   ____  ____  ____   ___  
 ___| |__   ___  ___| |_|___ \|  _ \| __ ) / _ \ 
/ __| '_ \ / _ \/ _ \ __| __) | | | |  _ \| | | |
\__ \ | | |  __/  __/ |_ / __/| |_| | |_) | |_| |
|___/_| |_|\___|\___|\__|_____|____/|____/ \___/ 
                                                 

usage: sheet2dbo.py [-h] [-v] [-d] [-i INPUT]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase the verbosity level
  -d, --debug           print debug information
  -i INPUT, --input INPUT
                        input Excel sheet file name
```

## Reference

* [UDMI](https://github.com/faucetsdn/udmi)
* [UDMI site model](https://github.com/faucetsdn/udmi_site_model)
* [Digital Buildings Ontology](https://github.com/google/digitalbuildings)
