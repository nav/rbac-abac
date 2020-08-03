# RBAC-ABAC

An example implementation of Role Based Access Control and Attribute Based 
Access Control using [Python](https://github.com/casbin/pycasbin) 
implementation of [Casbin](https://casbin.org/).


## Components

There are three main files in the project:
 - model.conf
 - policy.csv
 - entities.py
 - conftest.py
 - tests.py
 
### model.conf

This file contains the model defintion and rules to be used to enforce
policies defined in the `policy.csv` file.

### policy.csv

This file contains all the policies that can be applied when enforcing
set of rules defined in the file above.

### entities.py

This file contains Entites to be used in the authorization domain.

### conftest.py

This file contains test fixtures used by `pytest`.


### tests.py

This file contains tests  to verify and validate rules evaluated by 
Casbin engine.


## Run tests


``` sh
pipenv install --dev
pipenv shell
pytest tests.py
```
