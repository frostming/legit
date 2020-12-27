"""
legit.bootstrap
~~~~~~~~~~~~~~~

This module boostraps the Legit runtime.
"""


from clint import resources
from clint.textui import colored
import crayons
import configparser

from .settings import legit_settings

resources.init('kennethreitz', 'legit')

try:
    config_file = resources.user.open('config.ini', 'r')
except OSError:
    resources.user.write('config.ini', '')
    config_file = resources.user.open('config.ini', 'r')


# Load existing configuration.
config = configparser.ConfigParser()
config.read_file(config_file)


# Populate if needed.
if not config.has_section('legit'):
    config.add_section('legit')


modified = False

# Set defaults if they are missing.
# Add everything to settings object.
for (k, v, _) in legit_settings.config_defaults:
    if not config.has_option('legit', k):
        modified = True
        config.set('legit', k, v)
        setattr(legit_settings, k, v)
    else:
        val = config.get('legit', k)

        # Map boolean strings.
        if val.lower() in ('true', '1', 'yep', 'sure'):
            val = True
        elif val.lower() in ('false', '0', 'nope', 'nadda', 'nah'):
            val = False

        setattr(legit_settings, k, val)

if modified:
    config_file = resources.user.open('config.ini', 'w')
    config.write(config_file)


if legit_settings.disable_colors:
    crayons.disable()
    colored.DISABLE_COLOR = True
