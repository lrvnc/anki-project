# 1.Authenticate
apikey = 'FVbakscJ2HHC1t-7eV9pJfr2GHinLEHA9319j_YQEIs8'
url = 'https://api.us-south.language-translator.watson.cloud.ibm.com/instances/7e702dd5-51bc-47a0-822a-faed09fa3919'

# import deps
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# Setup service
authenticator = IAMAuthenticator(apikey)
lt = LanguageTranslatorV3(version='2018-05-01', authenticator=authenticator)
lt.set_service_url(url)

# 2. Translate
ans = lt.translate(text="comprendre", model_id='fr-en').get_result()
fren = ans['translations'][0]['translation']

print('fr -> en: ', fren)

ans = lt.translate(text=fren, model_id='en-pt').get_result()
enpt = ans['translations'][0]['translation']

print('en -> pt: ', enpt)
