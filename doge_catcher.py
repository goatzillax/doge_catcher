import sys, getopt
from mvextractor.videocap import VideoCap

from PIL import Image
import PIL.ImageOps

#  bitmap mask file is black on white because it's easier to draw that way, so invert it for actual use
#  i.e. in the script black is 0, aka "do not search"
mask = PIL.ImageOps.invert(Image.open("mask.bmp"))

f = sys.argv[1]

vc = VideoCap()
vc.open(f)

frame = 0  #  this is probably not useful, will have to check.  timestamps more useful butt complicated

max_mv = [0, 0]

# mv indices
src_x = 3
src_y = 4
dst_x = 5
dst_y = 6
motion_x = 7
motion_y = 8

while True:
   retval = vc.read()

   if not retval[0]:
      break

   frame += 1

   if retval[3] not in ["I","P"]:
      print("wack frame found")

   mv_cnt = 0
   sum = [0, 0] # so anything moving left should result in a large-ish positive X

   for mv in retval[2]:
      if not (mv[0] < 0):
         print("future frame reference found")
         continue
      if not (mv[9] == 4):  #  seems like the subpixel resolution is fixed at 1/4 or whatever
         print("motion_scale != 4")
         continue

      # alright if we managed to survive the gauntlet let's do this.
      mv_cnt += 1

      # Origin appears to be top left
      # still kind of shitty, but a more advanced kind of shitty
      try:
         search = (mask.getpixel((mv[src_x],mv[src_y])) != 0) and (mask.getpixel((mv[dst_x],mv[dst_y])) != 0)
         if search:
            sum[0] += mv[motion_x]
            sum[1] += mv[motion_y]
      except:
         pass #  WOW there are a lot of MV's right at 1080 for some reason
         #print("ERROR:  bad getpixel src=(%d,%d) dst=(%d,%d)" % (mv[src_x],mv[src_y],mv[dst_x],mv[dst_y]))

   if (mv_cnt):
      #  should probably have an upper bounds too unless turbo doge vtec kicked in yo
      if (sum[0] > 1000):
         print("frame %6d: mv_cnt %d vector sum (%d, %d)" % (frame, mv_cnt, sum[0], sum[1]))
      if sum[0] > max_mv[0]:
         #  DGAF about Y right now
         max_mv[0] = sum[0]  #  a new record!
         #print("frame %6d max_mv x: %d" % (frame, max_mv[0]))


