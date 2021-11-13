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
    print("Waiting for IP Assignment..")
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