import os
import sys
import site

# Add virtualenv site packages
site.addsitedir(os.path.join(os.path.dirname(__file__), 'env/local/lib64/python2.7/site-packages'))

# Path of execution
sys.path.append('/var/www/html/boost')

# Fired up virtualenv before include application
activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'env/bin/activate_this.py'))
execfile(activate_env, dict(__file__=activate_env))

# import boost as application
from boost import app as application