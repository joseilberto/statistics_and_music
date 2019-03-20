# Statistical analysis of (classical) music #

This repository is aimed to get songs in midi format, process them extracting
notes, channels, times and pitch. In an important remark is that we are willing
to work with piano midi file only. The data was mainly collected in [Classical
Piano Midi Page](http://www.piano-midi.de/midi_files.htm).

## Requirements ##

All requirements are available in requirements.sh file. But basically, it creates
a pyenv environment with libraries for web crawling the main Classical Piano
Midi Page, process the midi to a csv file with specified data and then get the
statistics for each file.

```
sh requirements.sh
source env/bin/activate
```
