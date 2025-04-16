from setuptools import find_packages, setup

package_name = 'gpt'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    include_package_data=True, 
    package_data={
        'gpt': ['prompt.txt','audio_files/*'],  # Specify the file to include
    },
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/audio_files', ['audio_files/init.wav', 'audio_files/conf.wav']),  # Add audio files explicitly
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
            'gpt_node = gpt.gpt:main',
            'audio = gpt.audio:main'
        ],
    },
)
