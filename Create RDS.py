#Create RDS Instance, Start, Stop and Terminate
#Created By Christopher Howard

import boto3
import time
rds = boto3.client('rds')
dbid = 'chdb-instance-1'
checkInterval = 10

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
        time.sleep(checkInterval)
        print(rds.describe_db_instances(DBInstanceIdentifier=dbid )['DBInstances'][0]['DBInstanceStatus'])
        
print(dbid + ' is now Available');
print(' ')
print('Now Stopping ' + dbid);
print(' ')
result = rds.stop_db_instance(
    DBInstanceIdentifier=dbid
)
print('DB Status: ' + result['DBInstance']['DBInstanceStatus'])

while(rds.describe_db_instances(DBInstanceIdentifier=dbid )['DBInstances'][0]['DBInstanceStatus']!='stopped'):  #Check for stopped State
        time.sleep(checkInterval)
        print(rds.describe_db_instances(DBInstanceIdentifier=dbid )['DBInstances'][0]['DBInstanceStatus'])

print(dbid + ' is now Stopped');
print(' ')
print('Now Deleting ' + dbid);
print(' ')
        
finalresponse = rds.delete_db_instance(
    DBInstanceIdentifier=dbid,
    SkipFinalSnapshot=True,
    DeleteAutomatedBackups=True
)

print('DB Status: ' + finalresponse['DBInstance']['DBInstanceStatus'])

if(finalresponse['DBInstance']['DBInstanceStatus']=='deleting'):
    print(dbid + ' is being deleted. We are Done!')