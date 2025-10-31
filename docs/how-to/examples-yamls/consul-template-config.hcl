vault {
  renew_token = false
  vault_agent_token_file = "/home/vault/.vault-token"
  retry {
    backoff = "1s"
  }
}

template {
  destination = "/etc/citrix/.env"
  contents = <<EOH
  {{- with secret "secret/citrix-adc/credential" }}
  NSUSERNAME={{ .Data.data.username }}
  NSPASSWORD={{ .Data.data.password }}
  {{ end }}
  EOH
}