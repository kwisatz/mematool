python setup.py egg_info
python setup.py bdist_egg

virtualenv/bin/easy_install -U dist/MeMaTool-0.1dev-py2.7.egg

sudo service uwsgi restart mematool
