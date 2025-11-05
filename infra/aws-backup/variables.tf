variable "aws_region" {
  type    = string
  default = "eu-west-1"
}


variable "app_name" {
  type    = string
  default = "smartticketai"
}

variable "vpc_id" {
  description = "VPC ID for deployment"
}

variable "subnets" {
  description = "Public subnets for ECS + Load Balancer"
  type        = list(string)
}
