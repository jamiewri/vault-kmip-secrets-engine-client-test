# Testing HashiCorp Vault's KMIP Secrets Engine
The purpose of this repoository is to use the OpenKMIP library to functionally test HashiCorp Vaults KMIP Secrets Engine

## Dependancies
- `Vault v1.8.1+ent`
- `Terraform v1.0.7`
- `jq-1.6`

## High level steps
1. Start Vault server
2. Configure Vault KMIP Secret Engine with Terraform
3. Generate and export KMIP credentials
4. Run KMIP Functional test

## Example test
Start the Vault server in one terminal
```
vault server -dev -dev-root-token-id="root"
```

In a new terminal enable Vault audit logs
```
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
vault audit enable file file_path=stdout
```

Configure the KMIP Secrets Engine in Vault
```
terraform init
terraform apply -auto-approve
```

Create and export KMIP client key
```
vault write \
  -format=json \
  kmip/scope/scopename/role/rolename/credential/generate \
  format=pem > src/credential.json

jq -r .data.certificate < src/credential.json > src/cert.pem
jq -r .data.private_key < src/credential.json > src/key.pem
jq -r '.data.ca_chain[]' < src/credential.json > src/ca.pem
```

Run KMIP Test
```
docker run \
  --env KMIP_ADDR=<IP Address> \
  --env KMIP_PORT=5696 \
  --env KMIP_CERT=cert.pem \
  --env KMIP_KEY=key.pem \
  --env KMIP_CA=ca.pem \
  --volume ${PWD}/src:/usr/src/app \
  vault-kmip-test
```


## Local Developement
MacOS
```
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
```
