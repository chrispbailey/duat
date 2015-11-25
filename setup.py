import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-duat',
    version='1.0',
    packages=['duat'],
    include_package_data=True,
    license='MIT License',
    description='A lightweight Django User Acceptance Testing feedback tool.',
    long_description=README,
    author='Chris Bailey',
    author_email="chris.p.bailey@gmail.com",
    url='https://github.com/chrispbailey/duat/',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Topic :: Software Development :: Testing',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
