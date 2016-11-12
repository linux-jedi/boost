activate_this = '/var/www/prod/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/html/boost')

from boost import app as application