from time import sleep


def run_file_ripper_once(definitions_file, definitions_format):
    print("running file ripper")


def run_file_ripper_continuously(definitions_file, definitions_format, interval_minutes=5):
    while True:
        run_file_ripper_once(definitions_file, definitions_format)
        sleep(60 * interval_minutes)
