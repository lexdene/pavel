import os
import pavel

DIRPATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'sources'
)


def _file_content(path):
    with open(path, 'r') as f:
        content = f.read()

    return content


def execute_file(name):
    path = os.path.join(
        DIRPATH,
        name + '.pvl'
    )
    return pavel.execute_code(_file_content(path))
