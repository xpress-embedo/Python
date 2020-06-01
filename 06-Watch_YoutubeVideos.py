import os
# In some cases when VLC installation folder is not detected, manually provide this.
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

import pafy
import vlc
import time
import datetime

num = 0
momo_chutney = "https://www.youtube.com/watch?v=4wSn3BmCQ-U"
grilled_sandwich = "https://www.youtube.com/watch?v=TVGzJfiTq_k"
kadi = "https://www.youtube.com/watch?v=uLLaIr-KXF8"
momo = "https://www.youtube.com/watch?v=bmwwlTLh2Gw"
rajma = "https://www.youtube.com/watch?v=AMLbgX6p1Ho"

urls = [ kadi, momo_chutney, grilled_sandwich, momo, rajma]

for i in range(600):
    for url in urls:
        video = pafy.new(url)
        best = video.getbest()
        # duration = video.duration
        # h,m,s = duration.split(':')
        # duration = int(datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)).total_seconds())
        duration = video.length
        print ("Video Title ", video.title)
        print ("Duration is ", duration )
        media = vlc.MediaPlayer( best.url )
        print ("Starting Player....")
        media.play()
        num = num+1
        # Add 20 seconds Buffer
        time.sleep( 60+20 )
        print ("Stoping Player....")
        media.stop()
        print ("Number of videos played = ", num )

    print ("REPETION COUNTER = ", i+1 )

print ("END")

# Shutdown the computer when script is completed
# os.system('shutdown -s')
