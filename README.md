# power service trade report generation application

## 🔁 Setup
### Step 1: Download and install the Anaconda / Miniconda distribution of Python
[anaconda installer](https://www.anaconda.com/products/distribution)


### Step 2: Create Conda virtual environment 
Create a Conda Environment (open Conda prompt):
```conda create --name ptl python=3.7```

### Step 3: Activate virtual environment
Activate the environment:
```conda activate ptl```

### Step 4: Install libraries
```pip install -r requirements.txt```


### Step 5: Configure databricks-connect
To setup databricks-connect then run:
```databricks-connect configure```



## ⚙️ Unit Test execution - 
 > Open Anaconda command prompt  (or VSCode Terminal) 
 > type “pytest” from the project root folder
 > press enter

### OR 
```pytest .\tests\power_service_test.py ```


## 📈 Packaging into a Wheel
 > Open Anaconda command prompt  / Powreshell prompt (or VSCode Terminal) 
 > Navigate to the project root folder within Virtual environment
 > execute below commad ; 
 ``` python setup.py bdist_wheel ```

## 🗒 Build
  > Open Anaconda command prompt  / Powreshell prompt (or VSCode Terminal) 
  > Navigate to the project root folder within Virtual environment
  > execute  ```.\Build.ps1 ```

## 🗒 Deploy from local
  > Open Anaconda command prompt  / Powreshell prompt (or VSCode Terminal) 
  > Navigate to the project root folder within Virtual environment
  > add MyBearerToken.txt file with access token added into it
  > execute  ```.\Deploy.ps1 ```

* **Build Wheel  Package **: wheel package is also uploaded into this Github repo, for refrence.
wheel file can be found at - ``` .\bin\power_service_pipelines_*.whl ```