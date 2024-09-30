# 压缩视频的工具
from moviepy.editor import VideoFileClip  # 导入VideoFileClip类

clip = VideoFileClip("static/videos/bg源.MP4")  # 载入原始视频

clip_resized = clip.resize(0.1)  # 缩放视频为原来的一半

clip_resized.write_videofile("大猫resize.MP4", audio_codec="aac")  # 写入文件，指定音频编码器为aac
