# JFK Assassination Files Download

This is a python script that will download all the JFK Assassination Files from the National Archive database without having to download them
individually.

If you look at the code for the project, you will see an array of URLs that have 3 indexes. The first being the main URL to the Nation Archives
where the release files live. Teh second index is how the script will process the content displayed on the National Archives website. The third
index is a number and is the total number of pages that list PDF files.

Being new to the the whole JFK Files, I put together this script in 10 minutes to download everything I know about. If there are more links on
the National Archives website, please let me know and I will update the script. For now, this project will only focus on downloading files from
the National Archives.

Over time, I will update the script to incorporate OCR, AI modeling for post processing and some other things to help work through the massive data
dump.

## Installation

You will need to have Python installed on your computer. Visit https://www.python.org/downloads/ to download Python. You will need to have
requests, and BeautifulSoup installed as well. You can do this using pip.

```bash
pip install requests
```

```bash
pip install BeautifulSoup
```

## Usage

Navigate to the root directory where you have downloaded this script. Run the following in command line or terminal.

```bash
python download.py
```

The script will start to download all the files it can find into the downloads directory. File names remain the same but files that may have the same name from different releases will be appended with "duplicate\_" and a random number. This is to preserve the file release integrity and to ensure all files are downloaded, even if they are duplicates since some files may be redacted and now have been un redacted.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
