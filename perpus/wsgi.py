import os
import sys

# Jalankan path ke direktori proyek Anda
path = '/home/Suryajulianputra/websekolah'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'perpus.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()