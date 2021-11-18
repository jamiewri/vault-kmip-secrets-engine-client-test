provider "vault" {
  address = "http://127.0.0.1:8200"
}

resource "vault_mount" "kmip" {
  path = "kmip"
  type = "kmip"
  description = "KMIP Secret Engine"
}

resource "vault_generic_endpoint" "kmip_config" {

  depends_on = [vault_mount.kmip]
  path = "kmip/config"
  ignore_absent_fields = true
  data_json = <<EOT
    {
    "listen_addrs": "0.0.0.0:5696",
    "default_tls_client_key_type": "rsa",
    "default_tls_client_key_bits": "2048",
    "default_tls_client_ttl": "172800",
    "server_hostnames": "vault,localhost,127.0.0.1"
    }
  EOT
}

resource "vault_generic_endpoint" "kmip_scope" {

 depends_on = [vault_generic_endpoint.kmip_config]
  path = "kmip/scope/scopename"
  ignore_absent_fields = true
  disable_read = true
  data_json = <<EOT
    {}
  EOT
}

resource "vault_generic_endpoint" "kmip_scope_role" {

  depends_on = [vault_generic_endpoint.kmip_scope]
  path = "kmip/scope/scopename/role/rolename"
  ignore_absent_fields = false
  disable_read = true
  data_json = <<EOT
    {
    "operation_all": true
    }
  EOT
}
