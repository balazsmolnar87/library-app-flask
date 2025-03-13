provider "aws" {
  region = "eu-central-1"
}

# VPC
data "aws_vpc" "default" {
  default = true
}

resource "aws_internet_gateway" "ebs_igw" {
  vpc_id = data.aws_vpc.default.id
}

data "aws_route_table" "default" {
  vpc_id = data.aws_vpc.default.id
}

resource "aws_route" "default_route" {
  route_table_id         = data.aws_route_table.default.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.ebs_igw.id
}

# IAM
resource "aws_iam_role" "beanstalk_ec2_role" {
  name = "aws-elasticbeanstalk-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "beanstalk_ec2_attach1" {
  role       = aws_iam_role.beanstalk_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSElasticBeanstalkMulticontainerDocker"
}

resource "aws_iam_role_policy_attachment" "beanstalk_ec2_attach2" {
  role       = aws_iam_role.beanstalk_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_instance_profile" "beanstalk_instance_profile" {
  name = "aws-elasticbeanstalk-ec2-profile"
  role = aws_iam_role.beanstalk_ec2_role.name
}

# Elastic Beanstalk
resource "aws_elastic_beanstalk_application" "flask_app" {
  name        = "flask-app"
  description = "Flask app deployed with Elastic Beanstalk"
}

resource "aws_elastic_beanstalk_environment" "flask_env" {
  name                = "flask-env"
  application         = aws_elastic_beanstalk_application.flask_app.name
  solution_stack_name = "64bit Amazon Linux 2 v4.0.8 running Docker"

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = aws_iam_instance_profile.beanstalk_instance_profile.name
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DOCKER_IMAGE"
    value     = "utamaro/library-app-flask:latest"  
  }

  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "SingleInstance"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "InstanceType"
    value     = "t3.small"
  }
}

# Output
output "elastic_beanstalk_url" {
  description = "URL of the deployed Flask app"
  value       = aws_elastic_beanstalk_environment.flask_env.endpoint_url
}
