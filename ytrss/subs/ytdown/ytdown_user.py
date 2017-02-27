from ytrss.subs.ytdown import YTdown_abstract

class YTdown_user(YTdown_abstract):
    def build_url(self):
        return "https://www.youtube.com/feeds/videos.xml?channel_id=%s" % self.code
