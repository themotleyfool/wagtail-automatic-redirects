from setuptools import setup, find_packages

install_requires = [
    'wagtail<2.0',
]

tests_require = []

setup(
    name='wagtail-automatic-redirects',
    description='Helpers for Wagtail Redirects',
    author='The Motley Fool',
    author_email='github@fool.com',
    url='https://github.com/themotleyfool/wagtail-automatic-redirects',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
    setup_requires=['setuptools_scm', ],
    use_scm_version=True,
)
