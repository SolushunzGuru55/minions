# CloudFormation-EC2 "Minions"

## The Story

As part of my Software Security classes, I wanted some way to create a certain
number of machines from scratch, mainly for penetration testing and other tasks
my students need to accomplish. The problem was, there was no easy way to create
many EC2 machines programatically. So I turned to my friend Daniel, who's an
expert in all things AWS, and he delivered with [this JSON code for CloudFormation](https://github.com/danielpizarro/cloudformation-examples). The
problem was that, if I needed to launch, say, 8 similar EC2 instances, I had to
make 8 `EC2Instance` sections on the JSON file, which is a painstaking,
error-prone process.

That's where [Troposphere](https://github.com/cloudtools/troposphere) came in.
With this powerful library I could create as many machines as I want. I can loop
(in Python ways) and generate the JSON file needed for stack creation.

## System Requirements

* Make
* Troposphere (you can install it using `pip install troposphere`)
* AWS CLI

## Usage

First, you need an AWS account, then, install AWS CLI following your
distribution's instructions. You will then need to configure AWS CLI for your
AWS IAM user following the instructions detailed
[here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) (as a security measure, NEVER provide your root account credentials).

Now, edit the `template_maker.py` file and modify the following:

* `NUMBER_OF_MACHINES`: The number of machines you want to launch.
* `INSTANCE_TYPE`: AWS EC2 instance type. If you are using the Free Tier,
`t2.micro` is good. For penetration testing, the minimum recommended instance
type is `t2.medium`
* `IMAGE_ID`: AMI image type. You can search for some Ubuntu images
[here](https://cloud-images.ubuntu.com/locator/ec2/).
* `KEY_PAIR_NAME`: You will need to create and then specify an EC2 keypair name
here.
* `PROVISSION_COMMANDS_LIST`: This is a list in which you will specify all the
commands (e.g., apt-get) for machine provission.

All you need to do now is run `make create_stack`, and it will be done. When
you want to delete the stack, run `make delete_stack`.

## Caveats

1. Each machine is assigned an Elastic IP (EIP) address. Each one of these
addresses has to be requested first. Amazon has a maximum of 5 EIP addresses
per region per user. If you need to create more than 5 machines, request
additional EIP addresses using
[this form](http://aws.amazon.com/contact-us/vpc-request/).
1. If you are going to use the machines for penetration testing, you should ask
for permission first to do so, since you maybe incurring in a policy violation.
Check [here](https://aws.amazon.com/security/penetration-testing/) for
instructions on how to get permission for penetration testing.
