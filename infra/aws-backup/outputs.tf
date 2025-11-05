output "load_balancer_dns" {
  value = aws_lb.app_lb.dns_name
}
