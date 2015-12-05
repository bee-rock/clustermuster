from setuptools import setup

setup(name='pycommandcenter',
      version='0.1',
      description='A simple web server that accepts commands over a web socket and distributes commands registered to the server over ssh.',
      url='https://github.com/bee-rock/pycommandcenter',
      author='Brock Hargreaves',
      author_email='brock@idevelopcode.com',
      license='MIT',
      packages=['pycommandcenter'],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
        'console_scripts': [
            'pycommandserver=sample:main',
        ],},)