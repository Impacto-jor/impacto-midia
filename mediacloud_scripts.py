import mediacloud


class MediaCloud:

    'Interage com a API do Facebook usando requests'

    def __init__(self, mediacloud_api):
        self._api = mediacloud.api.MediaCloud(mediacloud_api)

    def get_story_list(self, media_id, subject_list, start, end):
        """
            Usa o "media_id" do MediaCloud, uma lista de
            termos para a busca, uma data de início em datetime
            e uma data de fim
        """
        data = []
        if type(media_id) is not list:
            search_string = create_search_string(subject_list, media_id)
            stories = self._api.storyList(search_string,
                                          self._api.publish_date_query(start, end),
                                          last_processed_stories_id=0, rows=1000)
        else:
            stories = []
            for i in media_id:
                search_string = create_search_string(subject_list, i)
                info = self._api.storyList(search_string,
                                           self._api.publish_date_query(start, end),
                                           last_processed_stories_id=0, rows=1000)
                stories += info
        relevant = ['url', 'publish_date', 'title', 'stories_id', 'media_id']
        for story in stories:
            info = {k: v for k, v in story.items() if k in relevant}
            data.append(info)
        return data


# Helper functions
def create_search_string(subject_list, media_id):
    search_string = ''
    for word in subject_list:
        search_string += word
        if word != subject_list[-1]:
            search_string += ' OR '
    return f'{search_string} AND media_id:{media_id}'
