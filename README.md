# Testing the KMIP Secrets Engine
The purpose of this repoository is to use the OpenKMIP library to functionally test HashiCorp Vaults KMIP Secrets Engine

## Dependancies
- `Vault v1.8.1+ent`
- `Terraform v1.0.7`
- `jq-1.6`

## KMIP Client
MacOS
```
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
```

## HashiCorp Vault Server
Start the Vault server
```
vault server -dev -dev-root-token-id="root"
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
  format=pem > credential.json

jq -r .data.certificate < credential.json > cert.pem
jq -r .data.private_key < credential.json > key.pem
jq -r '.data.ca_chain[]' < credential.json > ca.pem
````


## HashiCorp Vault Client
```
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root
vault audit enable file file_path=stdout

```

## KMIP Client
```
python3 main.py -a AES -l 128  -s pykmip.conf
python3 get.py -s pykmip.conf  -i hrmw2GfsR51bxVuWkt5PXuwVAsTm3Xjs

```
