#Installs need modules for string analysis
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | sudo python
git clone https://github.com/translate/translate.git
cd translate
python setup.py install

