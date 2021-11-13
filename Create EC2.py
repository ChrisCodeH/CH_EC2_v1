#Create 2 EC2 Instances, Start, Tag, Check Status, Stop and Terminate
#Created By Christopher Howard

import boto3
import time
ec2 = boto3.resource('ec2')
#sts = boto3.client('sts')
#account_id = sts.get_caller_identity()['Account']

#create the ec2 instances
instances = ec2.create_instances(
     ImageId='ami-043e0add5c8665836',
     MinCount=1,
     MaxCount=2,
     InstanceType='t2.micro',
     KeyName='ec2-keypair',
 )
 
for instance in instances:
    print('Instance Created (ID): ' + instance.id)      
    
count=1
for instance in instances:
    #Debug Commands
    #instance_arn=f"arn:aws:ec2:{boto3.Session().region_name}:{account_id}:instance/{instance.id}"
    #print(instance_arn)
    #print(instance.public_ip_address)
    #print(instance.state)
    
    #Tag instances
    instance.create_tags(
    DryRun=False,
    Tags=[
        {
            'Key': 'project',
            'Value': str(count)
        },
    ]
    )
    count += 1
    
    #Check IPs
    print('Waiting for PIP assignment: ' + instance.id) 
    while(instance.public_ip_address==None):  #Keep Checking for PIP assignment
        time.sleep(5)
        instance.reload() 
        print("Waiting for IP Assignment..")
    
    print(' ') 
    print('################################') 
    print('Instance ID: ' + instance.id)    
    print('Public IP: ' + instance.public_ip_address)
    print('State: ' + instance.state.get('Name'))
    print('################################') 
    print(' ') 
    
#Wait for both instances to be in running state
for instance in instances:
    print('Checking for Run state: ' + instance.id) 
    while(int(instance.state.get('Code'))!=16):  #Check for Running State
        time.sleep(5)
        instance.reload() 
        print("Waiting for running state")
    print(instance.id + ' is running') 
    print(' ') 
    
print('Now Stopping and Terminating Instances..') 

for instance in instances:
    print('Stopping ' + instance.id) 
    instance.stop(
    Hibernate=False,
    DryRun=False,
    Force=True
    )
    
    while(int(instance.state.get('Code'))!=80):  #Check for Stopped State
        time.sleep(5)
        instance.reload() 
        print("Waiting for stop")
        
    print(instance.id + ' Stopped') 
    print(' ') 
    
    instance.terminate(
    DryRun=False
    )
    
    print("Terminating: " + instance.id)
    while(int(instance.state.get('Code'))!=48):  #Check for Complete Termination
        time.sleep(5)
        instance.reload() 
        print("Waiting for Termination")
    
    print(instance.id + ' Terminated') 
    print(' ') 
    
print('Done all ec2 instances terminated!')