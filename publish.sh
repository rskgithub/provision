#!/bin/bash +ex
git push github master --tags
python setup.py sdist upload
