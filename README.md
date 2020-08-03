# RBAC-ABAC

An example implementation of Role Based Access Control and Attribute Based 
Access Control using [Python](https://github.com/casbin/pycasbin) 
implementation of [Casbin](https://casbin.org/).


## Components

There are three main files in the project:
 - model.conf
 - policy.csv
 - tests.py
 
### model.conf

This file contains the model defintion and rules to be used to enforce
policies defined in the `policy.csv` file.

### policy.csv

This file contains all the policies that can be applied when enforcing
set of rules defined in the file above.

### tests.py

This file is a specification and implementation of Subjects, Resources, 
and Actions. It includes tests to verify and validate rules evaluated
by Casbin.


## Run tests


``` sh
pipenv install --dev
pipenv shell
pytest tests.py
```
