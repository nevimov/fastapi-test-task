#! /usr/bin/env bash
#
# Initialize the development environment.
#

this_script_dir=$(dirname "$0")

echo
echo "# WAITING FOR THE DATABASE TO START..."
./"$this_script_dir"/waitforit.sh $POSTGRES_HOST:$POSTGRES_PORT
echo

echo "# RUNNING MIGRATIONS..."
alembic upgrade head
echo

echo "# POPULATING THE DATABASE WITH INITIAL DATA..."
python "$this_script_dir"/populatedb.py
echo