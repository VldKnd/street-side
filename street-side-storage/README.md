# Webscrapper

We provide a short instruction on how to use the code provided in this github repository. All the commands written are supposed to be executed in the terminal of your OS. The code has been tested on MacOS and Linux, it might behave differently or **not work at all on windows OS**.

## The installation instructions.

 * **Install python**

The code is written in [python](https://docs.python.org/3/) programming language, you can read more about it on their official website. The installation instructions are [also provided on the website](https://www.python.org/downloads/).

 * **Install poetry**

The programm uses some non-standard python packages, to install them on your operating systyem the python package manager is needed. We are using [poetry](https://python-poetry.org/docs/) to handle all the python dependencies you might need. It has a command line interface, that is straight 
forward to use, but first you will have to install it. 

  For Linux, macOS, Windows (WSL) system, do:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
  To check, that the installation was succesful, you can run the following command to look at installed version of poetry.
```bash
poetry --version
> Poetry (version 1.5.1)
```

 * **Install python dependecies with poetry**

  Now we can install the python dependecies needed for the code to work. In your terminal navigate to the folder containing the package and execute (```cd``` command does not behave the same on Windows).

```bash
cd Webscraper
poetry install
```
  This will install the dependecies for the code to run. Wait for the installation to finish and run the code!

## Running the program

The main code is written in main.py file. 
```bash
> main.py --help
Webscrapping application.

options:
  -h, --help            show this help message and exit
  -f INPUT_FILE, --input-file INPUT_FILE
                        file with urls of websites to parse. (default: None)
  -v, --verbose         If -v is set the logs will be shown. (default: True)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output file path to save the results. It has to be *.csv or *.xlsx (default:
                        outputs/09_08_2023_11_32_output.xlsx)
```
You can run it with the following command
```bash
python main.py -f full_path_to_your_file -o full_path_to_save_output
```
for example
```bash
python main.py -f websites/one_website.json  -o outputs/output_example.xlsx
```
It will print some infromation about the process of webscrapping and if it was succesfully executed will create a file in ```path_to_save_output```.

**Note**
* The input file has to be in .xlsx or .json format, with standardize variables. You can check the examples of accepted input files in websites folder.
* For the moment the programm does not process the excel or pdf files and only accumulates information from csv files.
