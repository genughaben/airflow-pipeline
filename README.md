# airflow-pipeline

## How to 

### Requirements
* This tutorial assumes a Ubuntu installation (specifically: 18.04)
* Assumes pip is installed

### Install Airflow locally

#### Install and setup Postgresql DB
```
> sudo apt-get install postgresql postgresql-contrib

```
<to be continued. Based on https://medium.com/@taufiq_ibrahim/apache-airflow-installation-on-ubuntu-ddc087482c14>

Helpful also: https://medium.com/@srivathsankr7/apache-airflow-a-practical-guide-5164ff19d18b

#### Python and Airflow
```
> cd ~
> git clone https://github.com/genughaben/airflow-pipeline airflow
> cd ~/airflow
> conda create --name airflow python=3.6.6
> conda activate airflow
> pip install -r requirements.txt
```

#### airflow.cfg Adaptation
Change paths to match your base-path: i.e. home/<hour-username>/ everywhere applicable.
[core]
dags_folder = /home/<user_name>/airflow/dags
base_log_folder = /home/<user_name>/airflow/logs
sql_alchemy_conn = postgresql+psycopg2://<user_name>@localhost:5432/airflow
[celery]
broker_url = sqla+postgresql://<user_name>@localhost:5432/airflow
...
result_backend = db+postgresql://<user_name>@localhost:5432/airflow


### Setup

#### Setup Redshift cluster**

##### .aws
Add your AWS key and secret.

```
> cd ~/airflow/aws_redshift
> cp aws_template .aws
```
Now, open .aws and add your AWS credentials.

##### dwh.cfg
* Cluster setup works with given values, but you can customize them if you please

##### Trigger cluster setup
**NB: if you start this, you pay money as for the number of instances outlined in dwh.cfg**
Open a terminal window
```
    > cd aws_redshift
    > python setup_redshift 
```
Now, Wait for approx. 5-10min.  
Amongst other info the DWH_ENDPOINT is print out.  
This is required for table schema creation and for a redshift connection in airflow.

##### Create table schema:
* Copy the DWH_ENDPOINT from the terminal of the last step and enter it in dwh.cfg in section ETL for DWH_ENDPOINT, no quotes!

#### Setup local airflow

##### Start airflow
**Start the following code in three different terminal tabs:
```
> cd 
> conda activate airflow
> sudo service postgresql start
> cd ~/airflow
```

**Now start one of each commands in one of each tabs:**
* Tab 1:
```
> airflow webserver -p 8080
```
* Tab 2:
```
> airflow scheduler
```
* Tab 3:
```
> airflow worker
```

##### Configure Airflow via UI**
Open your local airflow installation on: localhost:8080/admin  
**Add Connections via Admin -> Connections**

#### 1. Connection: aws_credentials
* Conn ID: aws_credentials
* Conn Type: Amazon Web Services
* Login: your AWS Key
* Password: your AWS secret

#### 2. Connection: redshift
* Conn ID: redshift
* Conn Type: Postgres (might seem strange, but yes, Postgres is correct!)
* Schema: define your scheme (example: dwh_db; must be the same as you provision you AWS redshift instance with)
* Login: define a db user (example: dwh_user; must be the same as you provision you AWS redshift instance with)
* Password: define a db users password (must be the same as you provision you AWS redshift instance with)
* Port 5439


### Start

##### AWS Redshift
* You started the reshift cluster on setup.


Implements a basic airflow ETL pipeline for a fictional music streaming app.


Further reading about airflow and other workflow orchestrators:
* https://github.com/pditommaso/awesome-pipeline
* https://www.quora.com/Which-is-a-better-data-pipeline-scheduling-platform-Airflow-or-Luigi
* https://xunnanxu.github.io/2018/04/13/Workflow-Processing-Engine-Overview-2018-Airflow-vs-Azkaban-vs-Conductor-vs-Oozie-vs-Amazon-Step-Functions/
* https://medium.com/@cyrusv/luigi-vs-airflow-vs-zope-wfmc-comparison-of-open-source-workflow-engines-de5209e6dac1
* Monitoring tool: https://grafana.com/