from ytrss.subs.ytdown import YTdown_abstract

class YTdown_playlist(YTdown_abstract):
    def build_url(self):
        return "https://www.youtube.com/feeds/videos.xml?playlist_id=%s" % self.code
