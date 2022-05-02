from setuptools import find_packages ,setup

setup(
    name='byaddress',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4', 
    ],
    license='MIT'
    author='Promise Mwenga',
    author_email='promise_mwenga@hotmail.com',
    description='Webscrapes USPS website and validates addresses.'
)
