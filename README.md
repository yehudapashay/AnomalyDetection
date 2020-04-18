# Anomaly Detection on UAVs 
<p align="center">
    <img src="gui/images/anomaly_detection_logo.png">
</p>

System's main goal is to create machine learning models for anomaly detection on UAVs.
The system allows creation and loading of machine learning models by using dynamic inputs. <br/><br/>
Moreover, the system displays different output plots and evaluation metrics which compare between different models and the diagnosis of anomalies which were found.
Running the system with dynamic parameters will allow us to extract many different machine learning models.
Comparing them based on different evaluation metrics will lead to obtaining the best machine learning models for anomaly detection.<br/><br/>
Those models will be used as **a baseline for a real-time & light-weight anomaly detection algorithm based on streaming data from UAV sensors
in to order to get the earliest possible detection of GPS spoofing attacks on UAV’s.**

### Prerequisites

You should run the command (before run the system) in the console:

```
pip install -r requirements.txt
```

** See explanation below - Requirements File


## Getting Started

First, you should clone the project to your local environment:

```
git clone https://github.com/liorpizman/AnomalyDetection.git
```

<br/>

Run 'guiController.py' file in order to run the system.<br/>
<img src="utils/images/shared/guiController.JPG">

Choose Between two different option:<br/>
<img height=300 width=320 src="utils/images/shared/mainWindow.JPG">

### First Flow - Create new machine learning model

Insert simulated data / ADS-B data set input files<br/>
<img height=350 width=370 src="utils/images/new_model/newModelWindow.JPG">

Select algorithms for which you want to build anomaly detection models<br/>
<img height=350 width=370 src="utils/images/new_model/algorithmsWindow.JPG">

Select the values for each of the following parameters<br/>
<img height=350 width=370 src="utils/images/new_model/parametersOptionsWindow.JPG">

** See next step under the title: Both Flows - similarity functions step

### Second Flow - Load existing machine learning model

Insert input files for existing model<br/>
<img height=350 width=370 src="utils/images/load_model/loadModelWindow.JPG">

Insert paths for existing models<br/>
<img height=350 width=370 src="utils/images/load_model/existingsAlgorithmsWindow.JPG">

** See next step under the title: Both Flows - similarity functions step

### Both Flows - similarity functions step

Choose similarity functions from the following options<br/>
<img height=350 width=370 src="utils/images/shared/similarityOptionsWindow.JPG">

Loading model, please wait...<br/>
<img height=350 width=370 src="utils/images/shared/loadingWindow.JPG">

Choose an algorithm and a flight route in order to get the results<br/>
<img height=350 width=370 src="utils/images/shared/resultsWindow.JPG">

Choose an algorithm and a flight route in order to get the results<br/>
<img height=350 width=370 src="utils/images/shared/resultsTableWindow.JPG">

## Generated Machine Learning Models 

* LSTM - Long Short-Term Memory
* SVR - Support Vector Regression
* Random Forest
* Multivariate Linear Regression


| Algorithm | Description |
| -- | -- |
| LSTM | An artificial recurrent neural network (RNN) architecture used in the field of deep learning. |
| SVR | A popular machine learning tool for classification and regression. |
| Random Forest | Are supervised ensemble-learning models used for classification and regression. |
| Multivariate Linear Regression | An approach for statistical learning. As the name implies, multivariate regression is a technique that estimates a single regression model with more than one outcome variable. |
<br/>

## Train & Test Explained

| Data Set | Description |
| -- | -- |
| Train Set | Records containing sensors' values ​​for non-anomalous drone flights. |
| Test Set | Records containing sensors' values ​​for flights that have been attacked in various predefined attacks. |
<br/>

## GPS Spoofing Attacks - ADS-B Data Sets

| Attack | Description |
| -- | -- |
| Up attack | Try crushing the drone by changing his height sensor data in the dataset. |
| Down attack | An attempt to raise the drone up and get him out of his real route. |
| Fore attack | Randomly change sensors’ values. |
| Random attack | Injection of real sensors’ data from another flight to current flight. |
<br/>

## GPS Spoofing Attacks - Simulated Data Sets

| Attack | Description |
| -- | -- |
| Constant attack | Constant height and constant velocity. |
| Changing height attack | Constant height and changing velocity. |
| Changing velocity attack | Changing height and constant velocity. |
| Mixed attack | Changing height and changing velocity. |
<br/>

## LSTM - Results Example 

---- to do ----

## SVR - Results Example 

---- to do ----

## Random Forest - Results Example 

---- to do ----

## Multivariate Linear Regression - Results Example 

---- to do ----

## Research Risks

* **Imbalanced data sets** - the amount of data about attacks is very small compared to drone's regular behavior data.
* **Duration of the attack detection** - the true detection rate of GPS attacks will be high (TPR) but the duration of the attack detection will be long so the drone will be abducted even though the attack was detected.
* **Results expectations** – machine learning models results can be different from our initial expectations.


## Python Libraries We Used

* [Keras](https://keras.io/) - the Python Deep Learning library.
* [Scikit-learn](https://scikit-learn.org/) - is an open source machine learning library that supports supervised and unsupervised learning.

## Data Sets

* **ADS-B data sets** - automatic dependent surveillance – broadcast - data sets
* **Simulated data sets** - data sets which are generated by a simulator

## Requirements File

In order to create requirements.txt file we used **pipreqs** package.<br/>
**pipreqs** - Generate pip requirements.txt file based on imports of any project. (Automatically generate python dependencies)

**Why not use pip freeze ?** <br/><br/>
As the github repo of **pipreqs** says: [pipreqs Github repo](https://github.com/bndr/pipreqs)<br/>
1. **pip freeze** saves all packages in the environment including even those that you don't use in your current project.<br/>
2. **pip freeze** is harmful. Dependencies may be deprecated as our libraries are updated, but will then be left in our requirements.txt file with no good reason, polluting our dependency list.<br/><br/>
See the article [$ pip freeze > requirements.txt considered harmful](https://medium.com/@tomagee/pip-freeze-requirements-txt-considered-harmful-f0bce66cf895) 

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - the Python IDE for Professional Developers
* [Flightradar24](https://www.flightradar24.com/) - ADS-B data sets

## Authors

* **Lior Pizman** - *Final project, SISE, BGU* - [Github](https://github.com/liorpizman/)
* **Yehuda Pashay** - *Final project, SISE, BGU* - [Github](https://github.com/yehudapashay)

See also the list of [contributors](https://github.com/liorpizman/AnomalyDetection/contributors) who participated in this project.

