from setuptools import setup

setup(
    # The name of our pip package
    name='markus_script',
    # The Python packages in this project
    packages=[
        'markus_script',
    ],
    python_requires='>=3.5.2',
    include_package_data=True,
    install_requires=[
        'selenium',
    ],
    version="0.0.1",
    entry_points={
        'console_scripts': [
            # Link main() with shell command 'markus-script'
            'markus_script = markus_script.markus_script:main',
        ],
    },
)
