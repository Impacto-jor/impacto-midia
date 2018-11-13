import requests
import settings

token = settings.FACEBOOK_TOKEN

class FacebookRequest:

    'Interage com a API do Facebook usando requests'

    api_url = 'https://graph.facebook.com/v3.2/'

    def __init__(self, token):
        self._fb_token = token

    def url_stats(self, url):
        params = {
            'access_token': self._fb_token,
            'fields': 'og_object{image{url},title,description,created_time},engagement',
            'id': url
        }
        r = requests.get(self.api_url, params=params)
        data = r.json()
        print(data)
        #engagement = data['engagement']
        ####provisório para testar o app do site
        try:
            engagement = data['engagement']
        except KeyError:
            engagement = {'share_count': 0, 'reaction_count': 0}
        ####
        og_object = data.get('og_object', None)
        description = None
        if og_object:
            description = og_object.get('description', None)
        info = {"facebook_shares": engagement.get('share_count', 0),
                "facebook_reactions": engagement.get('reaction_count', 0),
                "description": description}
        return info
