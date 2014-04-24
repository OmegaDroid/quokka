from distutils.core import setup

setup(
    name='quokka',
    version='',
    packages=['utils', 'utils.templatetags', 'quokka', 'accounts', 'accounts.test', 'projects', 'projects.test',
              'projects.test.unit'],
    url='https://github.com/OmegaDroid/quokka',
    license='MIT',
    author='',
    author_email='',
    description='The happy little release animal.',
    requires=['django', 'django_parsley', 'django_taggit'],
)
