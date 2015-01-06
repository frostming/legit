# -*- coding: utf-8 -*-

"""
legit.bootstrap
~~~~~~~~~~~~~~~

This module boostraps the Legit runtime.
"""


from six.moves import configparser


import clint.textui.colored
from clint import resources
from clint.textui import colored



from .settings import settings



resources.init('kennethreitz', 'legit')

try:
    config_file = resources.user.open('config.ini', 'r')
except IOError:
    resources.user.write('config.ini', '')
    config_file = resources.user.open('config.ini', 'r')


# Load existing configuration.
config = configparser.ConfigParser()
config.readfp(config_file)



# Populate if needed.
if not config.has_section('legit'):
    config.add_section('legit')


modified = False

# Set defaults if they are missing.
# Add everything to settings object.
for (k, v, _) in settings.config_defaults:
    if not config.has_option('legit', k):
        modified = True
        config.set('legit', k, v)
        setattr(settings, k, v)
    else:
        val = config.get('legit', k)

        # Map boolean strings.
        if val.lower() in ('true', '1', 'yep', 'sure'):
            val = True
        elif val.lower() in ('false', '0', 'nope', 'nadda', 'nah'):
            val = False

        setattr(settings, k, val)

if modified:
    config_file = resources.user.open('config.ini', 'w')
    config.write(config_file)


if settings.disable_colors:
    clint.textui.colored.DISABLE_COLOR = True
