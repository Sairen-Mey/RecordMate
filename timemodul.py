import datetime



def get_date_and_time() -> str:
    return datetime.datetime.now().isoformat(
        sep=" ",
        timespec="seconds"
    )



def format_date_for_ui(date_str:str) -> str:
    dt = datetime.datetime.strptime(
        date_str,
        "%Y-%m-%d %H:%M:%S"
    )

    return dt.strftime(
        "%d.%m.%Y %H:%M:%S"
    )

