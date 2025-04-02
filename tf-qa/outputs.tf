output "load_balancer_dns_name" {
  value       = module.application.load_balancer_dns_name
  description = "The public DNS name of the load balancer"
}