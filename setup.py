from setuptools import setup


setup(name='pycommandcenter',
      version='0.1',
      description='A simple web server that accepts commands over a web socket and distributes commands registered to the server over ssh.',
      url='https://github.com/bee-rock/pycommandcenter',
      author='Brock Hargreaves',
      author_email='brock@idevelopcode.com',
      license='MIT',
      install_requires=['pyyaml>=3.11', 'argparse>=1.2.1', 'jsonschema>=2.5.1'],
      test_suite='nose.collector',
      tests_require=['nose>=1.3.7', 'mock>=1.3.0'],
      packages=['pycommandcenter'],
      entry_points={'console_scripts': ['pycommandserver=sample:main', ], }, )
