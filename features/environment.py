import os
import shutil


def before_feature(context, feature):
    if not os.path.exists('features/files'):
        os.mkdir('features/files')
    context.original_cwd = os.getcwd()
    file_path = os.path.join(os.getcwd(), 'features/files')
    os.chdir(file_path)


def after_feature(context, feature):
    try:
        path_to_delete = os.getcwd()
        os.chdir(context.original_cwd)
        shutil.rmtree(path_to_delete)
    except Exception as ex:
        print(ex)
