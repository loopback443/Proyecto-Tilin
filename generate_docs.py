import os
import sys
from pathlib import Path
import django
import pdoc

# Configurar entorno de Django
os.environ["DJANGO_SETTINGS_MODULE"] = "mi_proyecto.settings"
sys.path.insert(0, os.path.abspath("."))

# Iniciar Django
django.setup()

# Módulos a documentar
modules = ["cuentas.views", "cuentas.forms", "cuentas.urls","cuentas.models","cuentas.admin","cuentas.backend"]

# Generar documentación
pdoc.pdoc(*modules, output_directory=Path("docs"))
