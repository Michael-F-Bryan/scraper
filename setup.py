from setuptools import find_packages, setup
import versioneer


setup(
        name='scraper',
        pbr=True,
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        install_requires=[
            'requests',
            'bs4',
            'tqdm',
            'sphinx',
            'sphinxcontrib-napoleon',
            'sphinx_rtd_theme',
            ],

        )
