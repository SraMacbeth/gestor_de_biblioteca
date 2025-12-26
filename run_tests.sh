#!/bin/bash

# Activar el entorno virtual (opcional pero recomendado)
source venv/bin/activate

# Limpiar la base de datos de pruebas anterior para asegurar esquema nuevo
rm -f test_data/test_library.db

# Ejecutar el comando de pruebas
python3 -m unittest discover -v -s tests -p "test_*.py" -t .