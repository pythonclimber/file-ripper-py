import os


def after_scenario(context, scenario):
    try:
        os.remove(context.file.name)
    except Exception as ex:
        print(ex)
