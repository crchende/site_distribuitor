#!/bin/sh
echo "Activare venv:"
source ../.venv/bin/activate
echo "Configurare variabila mediu FLASK_APP"
export FLASK_APP=site_distribuitor
echo "Start server:"
exec flask run -h 0.0.0.0 -p 5010 --reload
