from keycloak.keycloak_openid import KeycloakOpenID

# Configure client1
keycloak_openid = KeycloakOpenID(server_url='http://[cluster1-ip]:8443/',
                                                client_id='[client-id]',
                                                client_secret_key='[secret]',
                                                realm_name='[realm-name]',
                                                verify = True
                                                )

keycloak_openid2 = KeycloakOpenID(server_url='http://[cluster2-ip]:8443/',
                                                client_id='[client-id]',
                                                client_secret_key='[secret]',
                                                realm_name='[realm-name]',
                                                verify = True
                                                )




# Get WellKnow
config_well_known = keycloak_openid.well_known()

# Get Token1
token = keycloak_openid.token("[user]", "[pass]")

test = token['refresh_token']

# Get Userinfo
# userinfo = keycloak_openid.userinfo(token['access_token'])

# Refresh token
# token = keycloak_openid.refresh_token(token['refresh_token'])

# Decode Token
KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid2.public_key() + "\n-----END PUBLIC KEY-----"
options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
token_info = keycloak_openid2.decode_token(token['access_token'], key=KEYCLOAK_PUBLIC_KEY, options=options)

print(token_info)
