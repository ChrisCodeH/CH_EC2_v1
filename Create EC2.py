import boto3
ec2 = boto3.resource('ec2')
sts = boto3.client('sts')
account_id = sts.get_caller_identity()['Account']

#create a new EC2 instance
instances = ec2.create_instances(
     ImageId='ami-043e0add5c8665836',
     MinCount=1,
     MaxCount=2,
     InstanceType='t2.micro',
     KeyName='ec2-keypair',
 )
 

count=1
for instance in instances:
    instance_arn=f"arn:aws:ec2:{boto3.Session().region_name}:{account_id}:instance/{instance.id}"
    print(instance_arn)
    print(instance.public_ip_address)
    print(instance.state)
    instance.create_tags(
    DryRun=False,
    Tags=[
        {
            'Key': 'project',
            'Value': str(++count)
        },
    ]
)