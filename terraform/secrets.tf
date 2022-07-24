resource "aws_secretsmanager_secret" "task_secrets" {
  name = "${local.environment}/${local.namespace}/secrets.json"
  description = "Secrets for the ${local.environment} project"
  recovery_window_in_days = 0
  tags = local.tags
}

resource "aws_secretsmanager_secret_version" "task_secrets_value" {
  secret_id     = aws_secretsmanager_secret.task_secrets.id
  secret_string = local.secrets_json
}
