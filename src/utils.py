import os

def path(relative_path):
    """
    Return an absolute path for a given relative path.
    Ensures compatibility across OS.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)

