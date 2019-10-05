# airflow-pipeline

## How to 

### Requirements
* This tutorial assumes a Ubuntu installation (specifically: 18.04)
* Assumes pip is installed

### Setup

**Install and setup Postgresql DB**
```
> sudo apt-get install postgresql postgresql-contrib

```
<to be continued. Based on https://medium.com/@taufiq_ibrahim/apache-airflow-installation-on-ubuntu-ddc087482c14>

**Python and Airflow**
```
> cd ~
> git clone https://github.com/genughaben/airflow-pipeline airflow
> cd ~/airflow
> conda create --name airflow python=3.6.6
> conda activate airflow
> pip install -r requirements.txt
```

**airflow.cfg Adaptation**
Change paths to match your base-path: i.e. home/<hour-username>/ everywhere applicable.

**.aws**
Add your AWS key and secret.

```
> cd ~/airflow/aws_redshift
> cp aws_template .aws
```
Now, open .aws and add your AWS credentials.

**Configure Airflow via UI**
Add Connections via Admin -> Connections

#### 1. aws_credentials
* Conn ID: aws_credentials
* Conn Type: Amazon Web Services
* Login: your AWS Key
* Password: your AWS secret

#### 2. redshift
* Conn ID: redshift
* Conn Type: Postgres [might seem strange, but yes, Postgres is correct!]
* Schema: define your scheme [example: dwh_db] [must be the same as you provision you AWS redshift instance with]
* Login: define a db user [example: dwh_user] [must be the same as you provision you AWS redshift instance with]
* Password: define a db users password [must be the same as you provision you AWS redshift instance with]
* Port 5439

### Start

##### AWS Redshift
<to be continued> 

##### Local airflow
```
> cd 
> conda activate airflow
> sudo service postgresql start
> cd ~/airflow
> bash start.sh
```

Implements a basic airflow ETL pipeline for a fictional music streaming app.
