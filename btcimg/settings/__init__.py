import os
import re

try:
    # Pulled from Honcho code with minor updates, reads local default
    # environment variables from a .env file located in the project root
    # directory by default, unless another env file is specified in
    env_file = os.environ.get('BTCIMG_ENV_FILE', '.env')
    with open(env_file, 'r') as f:
        for line in f:
            match = re.search(r'([A-Za-z_0-9]+)=(.*)$', line)
            if match:
                # if the value was wrapped in quotes strip them off
                key, val = match.group(1), match.group(2).strip('\'"')
                # only set the ENV variable if it has not already been defined
                os.environ.setdefault(key, val)
except IOError:
    pass


def local_join(*path):
    """
    Convenience function for path joining
    """
    return os.path.join(os.path.dirname(__file__), *path)


def django_compressor_manifest():
    """
    When a site is deployed, a COMMIT file is written with the commit hash of the
    code deployed. Using that file we can version the manifest used by
    django-compressor.

    With this default value, this configuration is safe in all environments.
    """
    try:
        with open(local_join('../../COMMIT'), 'r') as f:
            return 'manifest_{}.json'.format(f.read().strip())
    except IOError:
        return 'manifest_default.json'
