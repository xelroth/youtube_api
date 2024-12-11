from json import (
    loads as json_loads,
    dumps as json_dumps
)
from urllib import (
    parse as urllib_parse,
    request as urllib_request
)

class YouTubeInfoFetcher:
    def __init__(self):
        self.__api__ = "https://submagic-free-tools.fly.dev/api/youtube-info"

    def __fetch_info__(self, video_url):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = urllib_parse.urlencode({'url': video_url}).encode()
        req = urllib_request.Request(self.__api__, data=data, headers=headers)

        try:
            with urllib_request.urlopen(req) as response:
                return json_loads(response.read())
        except Exception as e:
            raise RuntimeError(f"Failed to fetch video info: {str(e)}")

class ResponseHandler:
    @staticmethod
    def send_response(status_code, message, additional_data=None):
        additional_data = additional_data or {}
        response = {
            'status': status_code,
            'result': {'message': message, **additional_data}
        }
        return json_dumps(response, ensure_ascii=False)

class YouTubeVideoProcessor:
    def __init__(self, video_link):
        self.video_link = video_link
        self.fetcher = YouTubeInfoFetcher()
        self.response_handler = ResponseHandler()

    def process_video(self):
        if not self.video_link:
            return self.response_handler.send_response(400, 'Video link is required!')

        try:
            response = self.fetcher.__fetch_info__(self.video_link)
            video_formats = [
                {
                    "label": item['label'],
                    "ext": item['ext'],
                    "height": f"{item['height']} p",
                    "url": item['url']
                } for item in response.get('formats', [])
            ]
            return self.response_handler.send_response(200, 'Operation successful', {
                'title': response['title'],
                'img': response['thumbnailUrl'],
                'result': video_formats
            })
        except RuntimeError as e:
            return self.response_handler.send_response(500, str(e))
def main():
    # this function is for TEST! You can remove the main function 
    video_link = 'https://youtu.be/QrxfKXJMu4s?si=C8q5obRfzeeuYl4C'
    return YouTubeVideoProcessor(video_link).process_video()

if __name__ == "__main__":
    main()
