# generate_docs.py
import os
import django
import pdoc
from pathlib import Path  # ✅ Importación necesaria

# Establece el módulo de configuración
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mi_proyecto.settings")
os.environ.setdefault("PYTHONPATH", ".")

# Inicializa Django
django.setup()

# Genera la documentación para la app 'cuentas'
pdoc.pdoc("cuentas", output_directory=Path("cuentas/docs"))
