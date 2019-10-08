from aws_manager import RedshiftCluster

if __name__ == "__main__":
    redshift_cluster = RedshiftCluster()
    redshift_cluster.shutdown()