import urllib,urllib2,cgi
import simplejson
from picplz.errors import PicplzError

def build_request_code_url(client_id,redirect_uri):
    request_url = "https://picplz.com/oauth2/authenticate?client_id=%s&response_type=code&redirect_uri=%s" %(client_id,redirect_uri)
    return request_url

def build_access_token_url(client_id,client_secret,redirect_uri,code):
    access_token_url = "https://picplz.com/oauth2/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=%s&code=%s" % (client_id,client_secret,redirect_uri,code)
    return access_token_url

class PicplzOauthToken():
    """ Object to represent picplz oauth tokens, since they call the secret 'oauth_secret' instead of 'oauth_token_scret' like everyone else """
    
    key = None
    secret = None

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
    
    def to_string(self):
        data = {
            'oauth_token': self.key,
            'oauth_secret': self.secret,
        }
        return urllib.urlencode(data)

    def from_string(s):
        """ Returns a token from something like:
        oauth_secret=xxx&oauth_token=xxx
        """
        params = cgi.parse_qs(s, keep_blank_values=False)
        key = params['oauth_token'][0]
        secret = params['oauth_secret'][0]
        token = PicplzOauthToken(key, secret)
        return token

    from_string = staticmethod(from_string)

    def __str__(self):
        return self.to_string()

class PicplzAuthenticator():
    
    client_id = None
    client_secret=None
    redirect_uri=None
    request_code=None
    access_token=None
    authenticated=False
    
    def __init__(self,picplz_client_id,picplz_client_secret,registered_redirect_uri,access_token=None):
        self.client_id = picplz_client_id
        self.client_secret = picplz_client_secret
        self.redirect_uri = registered_redirect_uri
        self.access_token = None
        if access_token is not None:
            self.access_token = access_token
        self.request_code = None
        
    def get_authorization_url(self):
        return build_request_code_url(self.client_id, self.redirect_uri)
    
    def get_access_token(self,code=None):
        if self.request_code is None and code is None:
            raise PicplzError("Authenticator does not have a valid request code and no code was passed in. A valid code is required to obtain an access token")
        
        if code is not None:
            self.request_code = code
            
        at_url = build_access_token_url(self.client_id, self.client_secret, self.redirect_uri, self.request_code)
        
        response = urllib2.urlopen(at_url)
        json = response.read()
        
        try:
            picplz_response = simplejson.loads(json)
            access_token_crazy_picplz_string = picplz_response['access_token']
            #why does this have '1|' in it? who knows... let's just deal with it
            access_token_string = access_token_crazy_picplz_string.split('|')[1]
            self.access_token = PicplzOauthToken.from_string(access_token_string)
            return self.access_token
        except:
            raise PicplzError("failed to obtain access token, picplz response was: %s" % (json))