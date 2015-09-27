import os

from distutils.core import setup

ROOT = os.path.dirname(os.path.realpath(__file__))
setup(
    name='wmsigner',
    version='0.1.0',
    url='https://github.com/egorsmkv/wmsigner',
    description='WebMoney Signer',
    long_description=open(os.path.join(ROOT, 'README.rst')).read(),
    author='Egor Smolyakov',
    author_email='egorsmkv@gmail.com',
    license='MIT',
    keywords='webmoney singer security wmsigner WMXI',
    packages=['wmsigner'],
    data_files=[('', ['README.rst'])],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
