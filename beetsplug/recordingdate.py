#!/usr/bin/env python

import musicbrainzngs
musicbrainzngs.set_useragent("Beets recording date plugin", "0.1", "http://github.com/tweitzel")

from beets.plugins import BeetsPlugin
from beets import autotag, library, ui, util, mediafile
from beets.autotag import hooks

class RecordingDatePlugin(BeetsPlugin):
    def __init__(self):
        super(RecordingDatePlugin, self).__init__()
        for recording_field in (u'recording_year', u'recording_month', u'recording_day'):
          field = mediafile.MediaField(
              mediafile.MP3DescStorageStyle(recording_field),
              mediafile.StorageStyle(recording_field)
          )
          self.add_media_field(recording_field, field)
    def commands(self):
        recording_date_command = ui.Subcommand('recordingdate', help="Retrieve the date of the first known recording of a track.", aliases=['rdate'])
        recording_date_command.func = self.func
        return [recording_date_command]

    def func(self, lib, opts, args):
        query = ui.decargs(args)
        self.recording_date(lib, query)

    def recording_date(self, lib, query):
        for item in lib.items(query):
            item_formatted = format(item)
            if not item.mb_trackid:
                self._log.info(u'Skipping track with no mb_trackid: {0}',
                               item_formatted)
                continue

            # Get the MusicBrainz recording info.
            recording_date = self.get_first_recording_year(item.mb_trackid)
            if not recording_date:
                self._log.info(u'Recording ID not found: {0} for track {0}',
                               item.mb_trackid,
                               item_formatted)
                continue
            # Apply.
            for recording_field in ('year','month','day'):
                write = False
                if recording_field in recording_date.keys():
                    item[u'recording_' + recording_field] = recording_date[recording_field]
                    write = True
                if write:
                    item.write()
                

    def _make_date_values(self, date_str):
        date_parts = date_str.split('-')
        date_values = {}
        for key in ('year', 'month', 'day'):
            if date_parts:
                date_part = date_parts.pop(0)
                try:
                    date_num = int(date_part)
                except ValueError:
                    continue
                date_values[key]=date_num
        return date_values

    def get_first_recording_year(self, mb_track_id):
        x = musicbrainzngs.get_recording_by_id(mb_track_id,includes=['releases'])
        oldest_release = {'year': None}
        for release in x['recording']['release-list']:
            release_date = self._make_date_values(release['date'])
            if oldest_release['year'] == None or oldest_release['year'] > release_date['year']:
                oldest_release = release_date
            elif oldest_release['year'] == release_date['year']:
                if 'month' in release_date.keys() and 'month' in oldest_release.keys() and oldest_release['month'] > release_date['month']: 
                        oldest_release = release_date
        return oldest_release



