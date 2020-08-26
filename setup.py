from setuptools import setup

setup(name='vtk_tools',
      version='0.1',
      description='supplemental tools for vtk cell calculations',
      url='https://github.com/data-exp-lab/vtk_tools',
      license='MIT',
      packages=['vtk_tools'],      
      install_requires=['vtk>=9.0.1','sympy','yt','numpy'],
      zip_safe=False)
