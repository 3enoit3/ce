
# publish data
rm -f db.sqlite3
ln -s Parser/codeData.sqlite3 db.sqlite3

# start server
python manage.py runserver 8080

