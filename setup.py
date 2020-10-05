import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
    setuptools.setup(
        name='file-ripper',
        version='1.1.0',
        author='Aaron Smith',
        author_email='asmitty92@gmail.com',
        license='MIT',
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=setuptools.find_packages(),
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',

        ]
    )

