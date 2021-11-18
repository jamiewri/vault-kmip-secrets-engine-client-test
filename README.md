# Testing HashiCorp Vault's KMIP Secrets Engine
The purpose of this repoository is to use the OpenKMIP library to functionally test HashiCorp Vaults KMIP Secrets Engine

## Dependancies
- `Vault v1.8.1+ent`
- `Terraform v1.0.7`
- `jq-1.6`

Although these are the specific binary versions that i used when testing, i would expect any Vault with the KMIP Secrets Engine to work.

## High level steps
1. Start Vault server
2. Configure Vault KMIP Secret Engine with Terraform
3. Generate and export KMIP credentials
4. Run KMIP Functional test

## Example test
Start the Vault server in one terminal.
```
vault server -dev \
   -dev-root-token-id="root" \
   -dev-listen-address=0.0.0.0:8200
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

Run KMIP Test with pre-build container
```
docker run \
  --env KMIP_ADDR=<IP Address> \
  --env KMIP_PORT=5696 \
  --env KMIP_CERT=cert.pem \
  --env KMIP_KEY=key.pem \
  --env KMIP_CA=ca.pem \
  --volume ${PWD}/src:/usr/src/app \
  jamiewri/vault-kmip-client-test:0.1


Config file ['/root/.pykmip/pykmip.conf', '/etc/pykmip/pykmip.conf', '/usr/local/lib/python3.7/site-packages/kmip/pykmip.conf', '/usr/local/lib/python3.7/site-packages/kmip/kmipconfig.ini'] not found
2021-11-18 03:25:21,517 - demo - INFO - Successfully created symmetric key with ID: 4L2Xc42pQo3V3QIBzFut37NLhZgtfKv6
2021-11-18 03:25:21,593 - demo - INFO - Successfully retrieved secret with ID: 4L2Xc42pQo3V3QIBzFut37NLhZgtfKv6
2021-11-18 03:25:21,593 - demo - INFO - Secret data: b'3ec8d789147fc436789a5ea2ecb5d7ba'
2021-11-18 03:25:21,634 - demo - INFO - Successfully retrieved 6 attribute names:
2021-11-18 03:25:21,634 - demo - INFO - Attribute name: Always Sensitive
2021-11-18 03:25:21,634 - demo - INFO - Attribute name: Extractable
2021-11-18 03:25:21,634 - demo - INFO - Attribute name: Never Extractable
2021-11-18 03:25:21,634 - demo - INFO - Attribute name: Object Type
2021-11-18 03:25:21,634 - demo - INFO - Attribute name: Sensitive
2021-11-18 03:25:21,634 - demo - INFO - Attribute name: State
2021-11-18 03:25:21,679 - demo - INFO - Successfully destroyed secret with ID: 4L2Xc42pQo3V3QIBzFut37NLhZgtfKv6
```

Excerpt from Vault Audit Logs
```
{"time":"2021-11-18T03:58:45.389287Z","type":"kmip-response","auth":{"token_type":"default"},"request":{"namespace":{"id":"root"},"data":{"kmip_request":
<..> 
[{"tag":"UniqueIdentifier","type":"TextString","value":"4L2Xc42pQo3V3QIBzFut37NLhZgtfKv6"}]
<...
```

KMIP Operations tested, in order of operation.
- operation_create
- operation_get
- operation_get_attribute_list
- operation_destroy


## Local Developement
MacOS
```
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Building the container from scratch
```
docker build -t vault-kmip-client-test .
```
