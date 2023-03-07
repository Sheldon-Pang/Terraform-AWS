
# Using Terraform to deploy AWS resources

This project is a demo for getting started with the Terraform for managing a base free-tier AWS resources, and automatically deploy and destroy resources with Python scripts.

### Project description

This project use [Terraform](https://www.terraform.io/) to managing AWS resources. 

Infrastructure managed in this project:

* [VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
* Public [Subnet](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#AddaSubnet) in the `VPC`
* [IGW](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html) to enable access to or from the Internet for `VPC`
* [Route Table](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html) to associate `IGW`, `VPC` and `Subnet`
* [EC2 Instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) in the public `Subnet` with the HTTP(s) & SSH access

### Required steps

1. [Install Terraform](https://learn.hashicorp.com/terraform/getting-started/install.html)
2. Create AWS account
3. If the file `~/.aws/credentials` does't exist, create it and add you Terraform profile to the file. For example: [More instruction](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
   ```text
   [default]
   aws_access_key_id = "Your access key"
   aws_secret_access_key = "Your secret access key"
   ```
4. Create S3 bucket to store Terraform state
    ```text
    aws s3api create-bucket --bucket "Your bucket name" --region us-east-1
    ```
5. Create config file `./free-tier/backend/config.tf` that will contain information how to store state in a given bucket. See [example](./free-tier/backend/example.config.tf). 
    ```text
    region  = "us-east-1"
    bucket  = "your_backet_name"
    key     = "terraform.tfstate"
    profile = "terraform"
    access_key = "Your access key"
    secret_key = "Your access key"
    ```
6. Create SSH key pair to connect to EC2 instance:
   ```bash
   cd ./free-tier/provision/access

   # it creates "free-tier-ec2-key" private key and "free-tier-ec2-key.pub" public key
   ssh-keygen -f free-tier-ec2-key
   ``` 
   
### Build infrastructure

1. `cd ./src/free-tier`
2. `terraform init -backend-config="./backend/config.tf"`
3. `terraform plan`
4. `terraform apply`

### Post steps

After building the infrastructure you can try to connect to you `EC2 instance` via SSH:

1. `cd ./free-tier`
2. `ssh -i ./provision/access/free-tier-ec2-key ubuntu@[EC2 public IP]`

To check HTTP access you can install `apache2` on your EC2 instance:

1. `sudo apt update && sudo apt install apache2` (on EC2 machine)
2. `sudo service apache2 start` (on EC2 machine) 
3. Check in browser: `http://[EC2 public IP]/`. You can see `Apache2 Default Page` (something like [this](https://annex.exploratorium.edu/))

### Make sure to destroy when you done testing
To destroy infrastructure:

1. `cd ./free-tier`
2. `terraform destroy`