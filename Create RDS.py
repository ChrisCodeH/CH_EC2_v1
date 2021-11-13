#Create RDS Instance, Start, Stop and Terminate
#Created By Christopher Howard

import boto3
import time
rds = boto3.client('rds')
dbid = 'chdb-instance-1'

response = rds.create_db_instance(
    AllocatedStorage=5,
    DBInstanceClass='db.t2.micro',
    DBInstanceIdentifier=dbid ,
    Engine='MySQL',
    MasterUserPassword='dbadmin!',
    MasterUsername='dbadmin',
)

print(response)
print('DB Status: ' + response['DBInstance']['DBInstanceStatus']);



#client.describe_db_instances(DBInstanceIdentifier='chdb-instance-1') 

while(rds.describe_db_instances(DBInstanceIdentifier=dbid )['DBInstances'][0]['DBInstanceStatus']!='available'):  #Check for Available State
        time.sleep(10)
        print(rds.describe_db_instances(DBInstanceIdentifier=dbid )['DBInstances'][0]['DBInstanceStatus'])
        
print(dbid + ' is now Available');
print(' ')
print('Now Stopping and Deleting' + dbid);
print(' ')
result = rds.stop_db_instance(
    DBInstanceIdentifier=dbid
)
print(result)

while(rds.describe_db_instances(DBInstanceIdentifier=dbid )['DBInstances'][0]['DBInstanceStatus']!='deleted'):  #Check for Available State
        time.sleep(10)
        print(rds.describe_db_instances(DBInstanceIdentifier=dbid )['DBInstances'][0]['DBInstanceStatus'])