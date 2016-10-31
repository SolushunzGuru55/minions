# Remember: EIP creation limit it 5. You have to request for more. See here:
# https://forums.aws.amazon.com/message.jspa?messageID=351512

from troposphere import Template, Output, Ref, Base64, GetAtt, Join
import troposphere.ec2 as ec2

NUMBER_OF_MACHINES = 2
INSTANCE_TYPE = 't2.micro'
IMAGE_ID = 'ami-840910ee'
KEY_PAIR_NAME = 'minions-keypair'
PROVISSION_COMMANDS_LIST = [
    'sudo apt-get -y update',
    'sudo apt-get -y install htop',
]

def get_user_data():
    string_list = list(PROVISSION_COMMANDS_LIST)
    string_list.insert(0, '#!/bin/bash -ex')
    string_list.append('# logs are in /var/log/cloud-init-output.log')
    string_list = [('%s\n' % element) for element in string_list]
    return Base64(Join('', string_list))


if __name__ == '__main__':

    template = Template()

    security_group = template.add_resource(
        ec2.SecurityGroup(
            'MySecurityGroup',
            GroupDescription='Enable SSH access and 8080 for web',
            SecurityGroupIngress=[
                ec2.SecurityGroupRule(
                    IpProtocol='tcp',
                    FromPort='22',
                    ToPort='22',
                    CidrIp='0.0.0.0/0'),
                ec2.SecurityGroupRule(
                    IpProtocol='tcp',
                    FromPort='8080',
                    ToPort='8080',
                    CidrIp='0.0.0.0/0'),
                ec2.SecurityGroupRule(
                    IpProtocol='tcp',
                    FromPort='8000',
                    ToPort='8000',
                    CidrIp='0.0.0.0/0'),
            ]
        )
    )

    for m in range(0, NUMBER_OF_MACHINES):

        ec2_instance = template.add_resource(
            ec2.Instance(
                ("EC2Instance%d" % m),
                ImageId = IMAGE_ID,
                InstanceType = INSTANCE_TYPE,
                KeyName = KEY_PAIR_NAME,
                SecurityGroups = [Ref(security_group)],
                UserData = get_user_data()
            )
        )

        eip = template.add_resource(
            ec2.EIP(
                ("EIP%d" % m),
                InstanceId = Ref(ec2_instance)
            )
        )


        template.add_output([
            Output(
                ("%dInstanceID" % m),
                Description = "Instance ID of the newly created EC2 instance",
                Value = Ref(ec2_instance),
            ),
            Output(
                ("%dPublicIP" % m),
                Description = "Public IP address of the newly created EC2 instance",
                Value = GetAtt(ec2_instance, "PublicIp"),
            ),
            Output(
                ("%dPublicDNS" % m),
                Description = "Public DNSName of the newly created EC2 instance",
                Value = GetAtt(ec2_instance, "PublicDnsName"),
            ),
        ])
    print(template.to_json())
