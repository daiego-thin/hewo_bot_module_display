from setuptools import find_packages, setup

package_name = 'hewo_bot_module_display'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Daiego43',
    maintainer_email='diedelcha@gmail.com',
    description='This package implements a pygame window that multimedia_display the robot\'s hewo. Since it is pygame, you could also use it to display whatever you want.',
    license='TODO',
    entry_points={
        'console_scripts': [
        ],
    },
)
