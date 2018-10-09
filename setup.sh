python3 setup.py
if [ -d "data" ]; then
  # Control will enter here if $DIRECTORY exists.
  rm -rf data
fi
mkdir data
cd data
sqlite3 mms.sqlite < ../db-schema.sql
