# Download PyInstaller

if [ ! -d pyinstaller-1.5.1 ]; then
	curl -o pyinstaller.tar.bz2 http://cloud.github.com/downloads/pyinstaller/pyinstaller/pyinstaller-1.5.1.tar.bz2
	tar xjf pyinstaller.tar.bz2
	rm -fr pyinstaller.tar.bz2
fi

# Virtualenv it up.
cd pyinstaller-1.5.1
virtualenv -p /usr/bin/python venv  --distribute
source venv/bin/activate
cd ../..

# Install depdendencies.
python setup.py develop
cd builders/pyinstaller-1.5.1

# Build this thing.
arch -i386 python ./Configure.py
arch -i386 python ./Makespec.py --onefile ../../legit_r
arch -i386 python ./Build.py legit_r/legit_r.spec

mkdir -p ../artifacts

mv legit_r/dist/legit_r ../artifacts/legit-darwin

echo 'Success!'
../artifacts/legit-darwin --version
