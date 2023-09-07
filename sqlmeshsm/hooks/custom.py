from importlib import util


def run_custom_hook(path: str):
    """Run a custom python file given the file path

    Args:
        path (str): Python file path
    """
    spec = util.spec_from_file_location("hook__custom", path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
