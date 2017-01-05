import os
import os.path
import sys

import pytest

# needed to get pretty assertion failures in unit tests:
if hasattr(pytest, 'register_assert_rewrite'):
    pytest.register_assert_rewrite('borg.testsuite')

# This is a hack to fix path problems because "borg" (the package) is in the source root.
# When importing the conftest an "import borg" can incorrectly import the borg from the
# source root instead of the one installed in the environment.
# The workaround is to remove entries pointing there from the path and check whether "borg"
# is still importable. If it is not, then it has not been installed in the environment
# and the entries are put back.

original_path = list(sys.path)
for entry in original_path:
    if entry == '' or entry == os.path.dirname(__file__):
        sys.path.remove(entry)

try:
    import borg
except ImportError:
    sys.path = original_path


@pytest.fixture(autouse=True)
def clean_env(tmpdir_factory, monkeypatch):
    # avoid that we access / modify the user's normal .config / .cache directory:
    monkeypatch.setenv('XDG_CONFIG_HOME', tmpdir_factory.mktemp('xdg-config-home'))
    monkeypatch.setenv('XDG_CACHE_HOME', tmpdir_factory.mktemp('xdg-cache-home'))
    # also avoid to use anything from the outside environment:
    keys = [key for key in os.environ if key.startswith('BORG_')]
    for key in keys:
        monkeypatch.delenv(key, raising=False)