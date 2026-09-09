import obsws_python as obs
import obs_config


class OBS_READER:
    def __init__(self):
        self.client = obs.ReqClient(
            host=obs_config.host,
            port=obs_config.port,
            password=obs_config.password,
            timeout=3
        )

    def get_record_status(self):
        return self.client.send("GetRecordStatus", raw=True)


obs_reader = OBS_READER()
