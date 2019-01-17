# first bump up package.json manually, commit and tag
python setup.py sdist
echo "RUN: twine upload dist/rodent-{VERSION}.tar.gz"
