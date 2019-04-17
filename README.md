# The Seek Notebook


<img src="https://seek4science.org/assets/images/seek-logo.svg" width="135px" height="132px">

<a href='https://coveralls.io/github/bogdan23a/TheSeekNotebook'><img src='https://coveralls.io/repos/github/bogdan23a/TheSeekNotebook/badge.svg' alt='Coverage Status' /></a><a href='https://theseeknotebook.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/theseeknotebook/badge/?version=latest' alt='Documentation Status' />
</a><img src="https://camo.githubusercontent.com/2091d99fb3b1ea0dcacb2ce564d5a3fc099c9ee7/68747470733a2f2f6261646765732e66726170736f66742e636f6d2f6f732f76322f6f70656e2d736f757263652e7376673f763d313032" width="120" height="20">

http://docutils.sourceforge.net/rst.html


## Introduction


## Getting Started

These instructions will show you how to get you a copy of the project up and how to execute the project.

### Before getting the package

First make sure that you have pip, conda, jupyter notebook, ipywidgets, pandas, requests and tabulate.
```
pip --version
conda --v
jupyter notebook --version
pip3 show ipywidgets
pip3 show pandas
pip3 show requests
pip3 show tabulate
```
And if you don't, install them.

#### The pip way

Get pip.
```
sudo apt update
sudo apt install python3-pip
pip3 --version
```

Then all the others.
```
pip3 install jupyter
pip3 install ipywidgets
pip3 install pandas
pip3 install requests
pip3 install tabulate
```

#### The conda way

Get conda.
```
curl -O https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh
bash Anaconda3-5.2.0-Linux-x86_64.sh
```

After you complete the installation quick-check it.
```
conda --version
```

Then all the others.
```
conda install jupyter
conda install ipywidgets
conda install pandas
conda install requests
conda install tabulate
```

In order to run this project you just need to have the SEEK.py file in the root of your project (or wherever).

### Cloning

Use this command to get a copy of the project:
```
git clone https://github.com/bogdan23a/TheSeekNotebook.git
```

### Running from the command line

To compile the project use:
```
mvn compile
```
To run the project use:
```
java -cp [PATH_TO_MYSQL_JAVA_CONNECTOR_JAR_FILE]:./target/classes Main
```

eg:
```
java -cp /home/bogdan/Downloads/mysql-connector-java-5.1.21.jar:./target/classes Main
``` 

### Testing

Run coverage via coverage.py with the following command(root dir):
```
coverage run --source=SEEK test.py TestSEEK
```

View your coverage via coverage.py with the following command(root dir):
```
coverage html -i
google-chrome docs/htmlcov/index.html
```
 
View your documentation via sphinx.py with the following command(root dir):
```
make clean html
google-chrome docs/build/html/index.html
```

## Sample I/O

Test 1:
```
Choose exercise (1/2):
1
TEST 1

Provide 2 strings to compare
First String:
D23W8MCCIZQOP9

Second String:
D236862CEZQOPS
5

```

Test 2:
```
Choose exercise (1/2):
2
TEST 2

Provide the department:
HQ General Management

Provide the pay type:
Monthly

Provide the education level:
Graduate Degree
