import os

def get_root_path():
    '''
    Get the absolute path to the repository root.
    Note that this function assumes that `config.py` is in src/config.py.
    '''
    root_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".."))
    
    return root_path
