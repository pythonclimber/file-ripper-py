import os


def before_scenario(context, scenario):
    if not os.path.exists('features/files'):
        os.mkdir('features/files')


def after_scenario(context, scenario):
    try:
        os.remove(context.file.name)
        os.rmdir('features/files')
    except Exception as ex:
        print(ex)
