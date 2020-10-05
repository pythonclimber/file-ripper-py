import os
import shutil


def before_scenario(context, scenario):
    if not os.path.exists('features/files'):
        os.mkdir('features/files')


def after_scenario(context, scenario):
    try:
        shutil.rmtree('features/files')
    except Exception as ex:
        print(ex)
