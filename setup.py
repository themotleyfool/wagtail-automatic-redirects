from setuptools import setup, find_packages

install_requires = [
    'wagtail',
]

tests_require = [
    'pytest-django',
    'wagtail-factories',
    'pytest',
]

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
        'Topic :: Software Development',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Wagtail',
    ],
    setup_requires=['setuptools_scm', 'pytest-runner'],
    use_scm_version=True,
)
