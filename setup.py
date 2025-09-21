'''
The setup.py file is an essential part of packaging and distribution python projects. It is used bu setuptools(or disuitls in order python versons) to define the configuration of u r project,such as its metadata, dependencies and more
'''

from setuptools import find_packages,setup
# find_package->scan folder and install libraries
from typing import List

def get_requirements():
    """
    This function will return list of requirements
    """
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            # read line
            lines=file.readlines()
            ## proces each line
            for line in lines:
                requirement=line.strip() #remove empty spaces
                # ignore empty lines and -e.
                if requirement and requirement!= '-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print('requirement.txt file not found')

    return requirement_lst

setup(
    name="Network Security",
    version="0.0.1",
    author="Syed Aftab",
    author_email="syed.mohd.aftab.2027@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)

# write the required in requirements.txt then after running pip install -r requirements.txt ,the -e . file will redirect to setup.py file will find all packages and download them