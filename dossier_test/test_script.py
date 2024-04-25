import subprocess

# Commandes Docker à exécuter
commands = [
    "docker pull toters/odoo:latest",
    "docker stop odoo || true",
    "docker rm odoo || true",
    "docker stop db || true",
    "docker rm db || true",
    "docker run -d -p 8069:8069 --name odoo toters/odoo:latest",
    "docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres --name db postgres:15"
]

# Boucle sur chaque commande et l'exécute
for command in commands:
    subprocess.run(command, shell=True)

