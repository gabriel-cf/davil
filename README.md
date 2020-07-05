# Introduction
DaViL is a data-visualization tool to visualize and manipulate multivariate data (i.e with more than 2 parameters) over a 2 dimensional plot.

To do so, it employs the popular technique based on radial axes called Star Coordinates. Each parameter is shown as an axis and the items of the file are mapped according to the value they present for each one.
All axes begin with the same length (weight) and can me moved freely in order to see the items moving transitioning to their new position.

![Davil Interface](https://i.imgur.com/xToSgOw.png)

By automatically positioning the axis, the tool also allows to perform automatic data classification operations by using clustering (K-Means) and techniques such as PCA and LDA:

## LDA
![Davil Interface - LDA](https://i.imgur.com/96dqq45.png)

## PCA and K-Means=3
![Davil Interface - K-Means and PCA](https://i.imgur.com/SGf0XTn.png)

# Technology Stack
Built in Python2.7, it uses Bokeh Server 0.12.3 as a base framwework for visualizing data in the browser and Flask to upload files and embed Bokeh into the website.

# Running Davil
The easiest way to run Davil is by running its Docker image as follows (note: the -DEMO tag simply adds a pre-loaded example file but it keeps all the functionality):

```sh
docker run -p 5000:5000 -p 5006:5006 niloxx/davil:0.2-DEMO
```

If you cannot run Docker, then simply follow the instructions on the next step to install the DEV version and run it.

# Installation (DEV)
If you want to contribute to the project (hurray!) then.. let's get started! This guide has been tested on Windows 64 bits machines, but it should be fairly similar for other OS.

Before you start you will need to set up for your local environment:
+ [Python 2.7 (Anaconda)](https://www.continuum.io/downloads)
+ [pip](https://pypi.python.org/pypi/pip)

Once you have that set up and the project cloned I recommend creating a virtual environment (just like for any other python project). [Here is how](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
Then simply run:

`pip install –r requirements.txt`
`conda install -c bokeh nodejs`

Now, time to test it: go to the root directory of the project and run the server:
`runserver.bat` or `./runserver.sh` if you are on Linux

Load one of the test files from the `sample_files` root directory.

**Enjoy!**