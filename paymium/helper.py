
import os
import sys


def get_script():
    return os.path.realpath(sys.argv[0])


def get_script_path(*args):
    return os.path.join(os.path.dirname(get_script()), *args)


def assert_status_ok(resp):
    if not resp.ok:
        raise AssertionError('Status != 2xx: ' + str(resp.headers))


def my_getenv(key):
    value = os.getenv(key)
    if value is None:
        raise AssertionError("Env variable: %s is not set" % key)
    return value
