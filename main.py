import obsws_python as obs
from obsws_python import ReqClient

import obs_config


class Note:
    def __init__(self, obs_timestamp:str, note_text:str):
        self.timestamp:str = obs_timestamp
        self.text:str = note_text

    def note_info(self):
        print(f"{self.timestamp}:{self.text}")

client = obs.ReqClient(
    host=obs_config.host,
    port=obs_config.port,
    password=obs_config.password,
    timeout=3
)

obs_record_status = client.send("GetRecordStatus", raw=True)

if obs_record_status['outputActive']:
    timestamp = obs_record_status['outputTimecode']
    text = "tratata"
    note = Note(obs_timestamp=timestamp, note_text=text)
    note.note_info()
else:
    print("record is not active")





#{'outputActive': False, 'outputBytes': 1275574, 'outputDuration': 0, 'outputPaused': False, 'outputTimecode': '00:00:00.000'}