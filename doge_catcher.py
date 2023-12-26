import sys, getopt
#import tracemalloc

from mvextractor.videocap import VideoCap

from PIL import Image
import PIL.ImageOps

#tracemalloc.start()

#  bitmap mask file is black on white because it's easier to draw that way, so invert it for actual use
#  i.e. in the script black is 0, aka "do not search"
mask = PIL.ImageOps.invert(Image.open("mask.bmp"))

bitmask = []
bitmask_w = mask.width
bitmask_h = mask.height
#  cool.  PIL apparently has a memory leak.  retarded.
for y in range(bitmask_h):
   for x in range(bitmask_w):
      bitmask.append(mask.getpixel((x,y)))

del(mask)

f = sys.argv[1]

vc = VideoCap()
vc.open(f)

frame = 0  #  this is probably not useful, will have to check.  timestamps more useful butt complicated

# mv indices
src_x = 3
src_y = 4
dst_x = 5
dst_y = 6
motion_x = 7
motion_y = 8

history = []

extract_framelist = []

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
         search = (bitmask[mv[src_x]+mv[src_y]*bitmask_w] != 0) and (bitmask[mv[dst_x]+mv[dst_y]*bitmask_w] != 0)
         if search:
            sum[0] += mv[motion_x]
            sum[1] += mv[motion_y]
      except:
         pass #  WOW there are a lot of MV's right at 1080 for some reason
         #print("ERROR:  bad getpixel src=(%d,%d) dst=(%d,%d)" % (mv[src_x],mv[src_y],mv[dst_x],mv[dst_y]))

   if (mv_cnt):
      #  should probably have an upper bounds too unless turbo doge vtec kicked in yo
      match = ""
      if (sum[0] > 1000):
         history.append((frame, sum))
         if len(history) > 6:
            history.pop(0)
         if len(history) == 6:
            if history[-1][0] - history[0][0] < 200:
               avg_y = 0
               for e in history:
                  avg_y += e[1][1]
               avg_y = avg_y / len(history)
               if avg_y <= 0:
                  match = "**"
                  #  fuck it, we'll do it live
                  #  actually should start marking frames starting from history[0][0]...
                  for tmp in range(history[0][0], frame):
                     if not tmp in extract_framelist:
                        extract_framelist.append(tmp)
                  #extract_framelist.append(frame)

         print("frame %6d: %2s mv_cnt %d vector sum (%d, %d)" % (frame, match, mv_cnt, sum[0], sum[1]))

#   if (frame % 100 == 0):
#      snapshot = tracemalloc.take_snapshot()
#      top_stats = snapshot.statistics('lineno')
#      for stat in top_stats[:10]:
#         print(stat)



# shit this is going to get nasty

FIRST=1;
if len(extract_framelist) > 0:
   filterfile = open("%s.filter" % (f[:-4]), "w")
   filterfile.write("select=")
   for fr in extract_framelist:
      if not FIRST:
         filterfile.write("+")
      else:
         FIRST=0
      filterfile.write("eq(n\\,%d)" % (fr))
   filterfile.close();
