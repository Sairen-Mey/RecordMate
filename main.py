import obsws_python as obs
import obs_config


class Note:
    def __init__(self, timestamp:str, text:str):
        self.timestamp:str = timestamp
        self.text:str = text


client = obs.ReqClient(host=obs_settings.host, port=obs_settings.port, password=obs_settings.password, timeout=3)




obs_record_status1 = client.send("GetRecordStatus", raw=True)
timestamp = obs_record_status1['outputTimecode']
text = str(input())
note = Note(timestamp=timestamp, text=text)

print(f"time: {note.timestamp} | text: {note.text}")


#{'outputActive': False, 'outputBytes': 1275574, 'outputDuration': 0, 'outputPaused': False, 'outputTimecode': '00:00:00.000'}