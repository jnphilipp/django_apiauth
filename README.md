# django_apiauth app


## Installation

Add django_apiauth to your INSTALLED_APPS

```
INSTALLED_APPS = (
    ...
    'django_apiauth',
)
```

To use default urls add the following to your urls.py.

```
urlpatterns = [
    ...
    url(r'^o/', include('django_apiauth.urls', namespace='django_apiauth')),
]
```


## Usage

Add the ```@authentication_required``` decorator to your functions that need authentication:

```
from django_apiauth.decorators import authentication_required

@authentication_required
def authenticated_users_only(request):
    """GET/POST parameters:
    token --- token: hash of user_id, secret and n,
              both secret and n were received by the authenticate request
    """
    # do stuff
    # request.user is authenticated user
    return HttpResponse()
```


### Authentication

#### Without applications

Authenticate via ```o/authenticate?user_id=USER_ID&password=PASSWORD``` where ```USERNAME``` is the required main user id e.g. username, email and ```PASSWORD``` is the password. Returned will either be a ```token``` or a ```secret``` and ```n```, depending on the settings of ```TOKEN_LIVE_TIME```.

* if ```TOKEN_LIVE_TIME``` is ```session``` a ```token``` will be return which needs to be given with each API request.
* if ```TOKEN_LIBE_TIME``` is ```request``` a ```secret``` and ```n``` will be return which will need to be hashed along with to user_id as the token for each request. After each request with a successful authentication ```n``` needs to be increased ```n = (n + 1) % 2147483647```.

```
import hashlib

token = hashlib.sha512(('%s%s%s' % (user_id, secret, n)).encode('utf-8')).hexdigest()
n = (n + 1) % 2147483647
```


#### With applications

When applications are used the authentication process has two steps.

1) ```o/request?user_id=USERNAME&client_id=CLIENT_ID``` where ```USERNAME``` is the required main user id e.g. username, email and ```CLIENT_ID``` is the id of the application. This request returns a timestamp which needs to be hash along with the application secret for the second request.

```
import hashlib
token = hashlib.sha512(('%s%s' % (application_secret, timestamp)).encode('utf-8')).hexdigest()
```

2) ```o/request?user_id=USERNAME&password=PASSWORD&client_id=CLIENT_ID&token=TOKEN&timestamp=TIMESTAMP``` where ```USERNAME``` is the required main user id e.g. username, email and ```PASSWORD``` is the password, ```CLIENT_ID``` is the id of the application, ```TOKEN``` is token from above and ```TIMESTAMP``` is the timestamp from the previous request. Returned will either be a ```token``` or a ```secret``` and ```n```, depending on the settings of ```TOKEN_LIVE_TIME```.

* if ```TOKEN_LIVE_TIME``` is ```session``` a ```token``` will be return which needs to be given with each API request.
* if ```TOKEN_LIBE_TIME``` is ```request``` a ```secret``` and ```n``` will be return which will need to be hashed along with to user_id as the token for each request. After each request with a successful authentication ```n``` needs to be increased ```n = (n + 1) % 2147483647```.

```
import hashlib

token = hashlib.sha512(('%s%s%s' % (user_id, secret, n)).encode('utf-8')).hexdigest()
n = (n + 1) % 2147483647
```


### Heartbeat

Heartbeat event ```o/heartbeat?token=TOKEN``` to prevent a user from being revoked out after ```AUTHED_USER_TIME``` of idle, defaults to one hour.


### Revoke

Revoke event ```o/revoke?token=TOKEN``` to revoke e.g. sign out a user.


## Settings
```
from django.utils import timezone
API_AUTH = {
    'REQUIRE_TWO_STEP_AUTHENTICATION': True,             # Require two step authentication even without applications
    'APPLICATIONS': False,                               # If true authentication is only possible with authorized applications
    'AUTH_REQUEST_TIME': timezone.timedelta(minutes=5),  # Maximum time between the two authentication request
    'AUTHED_USER_TIME': timezone.timedelta(hours=1),     # Default time after which a users authentication is revoked
    'TOKEN_LIVE_TIME': 'request',                        # One of 'session' or 'request': determents whether each request has a new token or only one per session
}
```
