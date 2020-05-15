# beets-recordingdate
Beets plugin that fetches earliest recording date per-track, ideal for greatest-hits albums

# Installation
1. clone this repository or download a zip and expand somewhere
2. open a command prompt or terminal
3. change to the directory containing the files
4. type: python3 setup.py install

# Configuration
auto:       Will run during an import operation if set to yes (default is yes)
force:      Re-process songs that have already been run through the plugin (default is no)
write_over: Also write to the year tag, erasing the original value (default is no)
relations:  A list of relation types to gather year values from (default: edit, first track release, remaster)
               For a list of acceptable values see: https://musicbrainz.org/relationships/recording-recording
               enter as a list like ['edit', 'first track release', 'remaster']
