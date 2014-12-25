import os
import pavel

DIRPATH = os.path.normpath(
    os.path.join(__file__, '../../examples')
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
