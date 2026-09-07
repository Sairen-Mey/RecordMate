import obsws_python as obs
import obs_config



client = obs.ReqClient(
    host=obs_config.host,
    port=obs_config.port,
    password=obs_config.password,
    timeout=3
)

def get_record_status():
    return client.send("GetRecordStatus", raw=True)
