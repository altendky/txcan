import setuptools
import versioneer


with open('README.rst') as f:
    readme = f.read()


extras_require_cli = [
    'click',
]


extras_require_test = [
    'coverage',
    'pytest',
    'pytest-cov',
    'tox',
]


setuptools.setup(
    name='txcan',
    author='Kyle Altendorf',
    description='Twisted, the way CANbus is supposed to be',
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='https://github.com/altendky/txcan',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='MIT',
    classifiers=[
        # complete classifier list:
        #   https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
    ],
    entry_points={
        'console_scripts': [
            'txcan = txcan.cli:main [cli]',
        ],
    },
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    install_requires=[
        'python-can',
        'twisted'
    ],
    extras_require={
        'cli': extras_require_cli,
        'dev': [
            'gitignoreio',
            *extras_require_cli,
            *extras_require_test,
        ],
        'test': extras_require_test,
    },
)
