from flask import Flask
import os
from azure.keyvault import KeyVaultClient
from msrestazure.azure_active_directory import MSIAuthentication, ServicePrincipalCredentials

app = Flask(__name__)

KEY_VAULT_URI = "https://ethosmetric.vault.azure.net/"


def get_key_vault_credentials():
    if "APPSETTING_WEBSITE_SITE_NAME" in os.environ:
        return MSIAuthentication(
            resource='https://vault.azure.net'
        )
    else:
        return ServicePrincipalCredentials(
            client_id=os.environ['AZURE_CLIENT_ID'],
            secret=os.environ['AZURE_CLIENT_SECRET'],
            tenant=os.environ['AZURE_TENANT_ID'],
            resource='https://vault.azure.net'
        )


@app.route("/")
def hello():
    return "Hello World!"


def test_vault():
    credentials = get_key_vault_credentials()
    kv_client = KeyVaultClient(
        credentials
    )

    key_vault_uri = KEY_VAULT_URI

    secret = kv_client.get_secret(
        key_vault_uri,
        "test",       
        "" 
    )
    return "secret value = {}".format(secret.value)

@app.route('/sshh')
def hello_world():
    try:
        return test_vault()
    except Exception as err:
        return str(err)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
