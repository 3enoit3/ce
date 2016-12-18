
# Create isolated env
cd ..
virtualenv ce
cd ce

# Install libs
source bin/activate
pip install Django
pip install djangorestframework
pip install beautifulsoup4
#pip install markdown       # Markdown support for the browsable API.
#pip install django-filter  # Filtering support

