#!/bin/bash

python3 manage.py loaddata ./fixtures/auth.json
for f in GestionDeInsumos GestionDeClientes \
GestionDeMascotas GestionDeTiposDeAtencion \
GestionDeServicios GestionDePracticas
do
  echo "Load $f"
  python3 manage.py loaddata ./Apps/$f/fixtures/$f.json
done