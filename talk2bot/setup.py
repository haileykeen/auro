from setuptools import find_packages, setup

package_name = 'talk2bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='syuhueihuang',
    maintainer_email='syuhuei.huang@ufl.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'explorer = talk2bot.talk2bot_explorer:main',
            'ultrasonic_avoidance = talk2bot.explorer_ultrasonic:main',
            'test_motion = talk2bot.test_motion:main',
        ],
    },
)
