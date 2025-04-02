output "load_balancer_dns_name" {
  value       = aws_lb.ecs_load_balancer.dns_name
  description = "The public DNS name of the load balancer"
}