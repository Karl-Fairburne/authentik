"""Discord OAuth Views"""
import json
from logging import getLogger

from requests.exceptions import RequestException

from passbook.oauth_client.clients import OAuth2Client
from passbook.oauth_client.source_types.manager import MANAGER, RequestKind
from passbook.oauth_client.utils import user_get_or_create
from passbook.oauth_client.views.core import OAuthCallback, OAuthRedirect

LOGGER = getLogger(__name__)


@MANAGER.source(kind=RequestKind.redirect, name='Discord')
class DiscordOAuthRedirect(OAuthRedirect):
    """Discord OAuth2 Redirect"""

    def get_additional_parameters(self, source):
        return {
            'scope': 'email identify',
        }


class DiscordOAuth2Client(OAuth2Client):
    """Discord OAuth2 Client"""

    def get_profile_info(self, raw_token):
        "Fetch user profile information."
        try:
            token = json.loads(raw_token)
            headers = {
                'Authorization': '%s %s' % (token['token_type'], token['access_token'])
            }
            response = self.request('get', self.source.profile_url,
                                    token=token['access_token'], headers=headers)
            response.raise_for_status()
        except RequestException as exc:
            LOGGER.warning('Unable to fetch user profile: %s', exc)
            return None
        else:
            return response.json() or response.text


@MANAGER.source(kind=RequestKind.callback, name='Discord')
class DiscordOAuth2Callback(OAuthCallback):
    """Discord OAuth2 Callback"""

    client_class = DiscordOAuth2Client

    def get_or_create_user(self, source, access, info):
        user_data = {
            'username': info.get('username'),
            'email': info.get('email', 'None'),
            'first_name': info.get('username'),
            'password': None,
        }
        discord_user = user_get_or_create(**user_data)
        return discord_user
