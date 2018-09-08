import setuptools


install_requires = ['PyYaml']

setuptools.setup(
    name="branch-history",
    version='0.1',
    description='Get checkout branch history',
    install_requires=install_requires,
    url='http://',
    author="Duhamel Ramanajafy",
    author_email="",
    license='MIT',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'git-branch-history = branch_history.__init__:main',
        ],
    },
    zip_safe=False,
)
