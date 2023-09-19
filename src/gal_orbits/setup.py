from setuptools import setup
from glob import glob
import os

package_name = 'gal_orbits'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'resource'), glob('resource/*.*'))
    ],
    install_requires=['setuptools', 'gdown', 'pandas'],
    zip_safe=True,
    maintainer='ros',
    maintainer_email='',
    description='Simple gal_orbits',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gal_orbits = gal_orbits.gal_orbits:main'
        ],
    },
)
