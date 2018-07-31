import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


path = os.path.dirname(os.path.abspath(__file__))


def package_files(directory):
    result = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filename = os.path.join(root, filename)
            result.append(os.path.abspath(filename))
    return result


setup(
    name="GoogleStorage",
    version="1.0",
    author="Madhan M",
    author_email="varadhodiyil@gmail.com",
    description="Google Cloud storage Wrapper",
    url="",
    packages=['GoogleStorage'],
    include_package_data=True,
    package_dir={'GoogleStorage': "src/"},
    package_data={'GoogleStorage': package_files('src/')},
)
