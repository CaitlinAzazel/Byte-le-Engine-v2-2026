rm vID
set -e
source .venv/bin/activate
python launcher.pyz client register --name $1 --uni $2 --team_type $3
