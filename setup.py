import setuptools
import os

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
requirements = list()

long_description = ('Обертка поверх Piki для построение микросервисов')

setuptools.setup(
    name='MRQservice',
    version='1.1.0',
    description='MRQservice - create micro-services',
    # long_description=open('README.rst').read(),
    maintainer='Zakirjanov Rinat M.',
    maintainer_email='rinat643@gmail.com',
    url='https://',
    packages=setuptools.find_packages(include=['MRQservices','MRQservices.*']),
    license='BSD',
    install_requires= open('./req.txt').read(),
    # package_data={'': ['LICENSE', 'README.rst']},
    extras_require={
        'pika': ['pika']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Communications', 'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking'
    ],
    zip_safe=True)