# Statistical analysis of (classical) music #

This repository is aimed to get songs in midi format, process them extracting
notes, channels, times and pitch. In an important remark is that we are willing
to work with piano midi file only. The data was mainly collected in [Classical
Piano Midi Page](http://www.piano-midi.de/midi_files.htm).

## Requirements ##

All requirements are available in requirements.sh file. But basically, it creates
a virtual environment with libraries for web crawling the main Classical Piano
Midi Page, process the midi to a csv file with specified data and then get the
statistics for each file.

```
sh requirements.sh
source env/bin/activate
```

## Usage ##

A run file is presented in this home folder with all the ETL process, extracting,
transforming midi files to csv and loading them to be processed. To run this
file, proceed as follows:
```
python run.py -p=/directory_to_save_midis/
```
