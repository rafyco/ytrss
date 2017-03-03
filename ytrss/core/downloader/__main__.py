from ytrss.core.downloader import Downloader

down = Downloader()

result = down.download("https://www.youtube.com/watch?v=YZuFsI-bttM")
if result:
    print("result: true")
else:
    print("result: false")
    
