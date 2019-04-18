# The Seek Notebook


<a href='https://coveralls.io/github/bogdan23a/TheSeekNotebook'><img src='https://coveralls.io/repos/github/bogdan23a/TheSeekNotebook/badge.svg' alt='Coverage Status' /></a><a href='https://theseeknotebook.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/theseeknotebook/badge/?version=latest' alt='Documentation Status' />
</a><img src="https://camo.githubusercontent.com/2091d99fb3b1ea0dcacb2ce564d5a3fc099c9ee7/68747470733a2f2f6261646765732e66726170736f66742e636f6d2f6f732f76322f6f70656e2d736f757263652e7376673f763d313032" width="120" height="20">


<img src="https://seek4science.org/assets/images/seek-logo.svg" width="135px" height="132px" align="right"><img src="https://upload.wikimedia.org/wikipedia/commons/3/38/Jupyter_logo.svg" width="135px" height="132px" align="right">



Building a Python Library for an E(lectronic)-Notebook implementing a scientific data catalog.

<details>
  <summary><strong>Table of Contents</strong> (click to expand)</summary>

<!-- toc -->
- [Background](#background)
- [Prerequisites](#prerequisites)
- [Clone](#cloning)
- [Import](#importing)
- [The Docs](#documentation)
- [Examples](#usage)
- [Testing](#testing)
- [Links](#links)
- [Contributing](#contributing)

<!-- tocstop -->

</details>

## Background

Bioinformatics is a broad science that involves working with a considerable supply of biological data and associates various groups of analysts and experts. Its practice involves the use of technology to do activities such as molecular biology modelling, image analysis, comparisons of linear sequences or 3D models and many other related tasks.

This project aims to satisfy the needs of people working in the field of bioinformatics. More specifically, people that work with scientific data towards a more analytical outcome and need to handle computational tools in order to get a conclusive view on their input.

This project intents to support the users by making the viewing, browsing and writing of reports, research, studies, etc, more accessible. 

## Prerequisites

These instructions will show you how to get you a copy of the project up and how to execute the project.

Before you get this package make sure that you have pip, conda, jupyter notebook, ipywidgets, pandas, requests and tabulate.
```bash
python setup.py install --user
```

Or you could use this command if you got the full copy of the project. 
```bash
pip install -r docs/requirements.txt
```

## Cloning

Just download the archive from git if you want to use just the provided package and the usage examples or use the following command to get a copy of the project if you want to contribute to the repository:
```bash
git clone https://github.com/bogdan23a/TheSeekNotebook.git
```

## Importing

In order to run this project you just need to have the SEEK.py file in the root of your project (or wherever). The you just have to import the package in your python or jupyter notebook files like so:
```python
import SEEK
```

## Documentation

Read the [documentation](https://theseeknotebook.readthedocs.io/en/latest/) for some other examples and further tips about the usage.

## Usage

* Authentication

Use the auth() method in order to create a login form and store them into a variable to use the credentials on the way.
```python
auth = SEEK.auth()
>>> Username: 
>>> Password:
```

* Reading

Use the read() class to create a reading object and use it to read, browse and download data from the HUB.
```python
r = SEEK.read(auth)
```

* DEFAULT Writing (on the testing DB)

Use the write() class to create a writing object and use it to write data to the testing HUB.
```python
w = SEEK.write(auth)
```

* OFFICIAL Writing

```python
w = SEEK.write(auth, "https://fairdomhub.org/")
```

<img src="https://github.com/bogdan23a/TheSeekNotebook/blob/master/docs/Usage.gif" width="1000px" height="400px">

## Testing

Run coverage via coverage.py with the following command(root dir):
```bash
coverage run --source=SEEK test.py TestSEEK
```

View your coverage via coverage.py with the following command(root dir):
```bash
coverage html -i
google-chrome htmlcov/index.html 
```
 
View your documentation via sphinx.py with the following command(root dir):
```bash
make clean html
google-chrome docs/build/html/index.html
```
## Links
JSON API to FAIRDOM SEEK on [Swagger Hub](https://app.swaggerhub.com/apis/FAIRDOM/SEEK/0.1).

Examples for the [SEEK API Workshop](https://github.com/FAIRdom/api-workshop).

More examples for the [SEEK API](https://github.com/bogdan23a/seekAPIexamples)

Use the [Testing](https://testing.sysmo-db.org/) platform for testing writing / creating capabilities.

## Contributing

**HELP WANTED** check out the [Contribution](CONTRIBUTING.md) instructions.

### Note to self
Should have taken a look into [FAIRDOMHub](docs/FAIRDOMHub:ARepositoryAndCollaboration.pdf) and [SEEK](SEEK:ASystemsBiologyDataAndModel.pdf) documents from day one, but don't always listen to me.
