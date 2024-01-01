from waifuc.source import DanbooruSource, LocalSource, VideoSource

# Crawl images from Danbooru
danbooru_source = DanbooruSource(['1girl'])

# Local images from directory '/your/directory'
local_source = LocalSource('/your/directory')

# Extract frames from videos in '/your/anime/directory'
video_source = VideoSource.from_directory('/your/anime/directory')
