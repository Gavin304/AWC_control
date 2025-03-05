from setuptools import find_packages, setup

package_name = 'tf_publisher'

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
    maintainer='gavin',
    maintainer_email='gavin.arpandy@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "tf_broadcaster.py = tf_publisher.tf_broadcaster:main",
            "tf2_broadcaster.py = tf_publisher.tf2_broadcaster:main",
        ],
    },
)
