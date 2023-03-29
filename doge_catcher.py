import sys, getopt
from mvextractor.videocap import VideoCap

f = sys.argv[1]

vc = VideoCap()
vc.open(f)

frame = 0  #  this is probably not useful, will have to check.  timestamps more useful butt complicated

bounds_topleft = [850, 75]
bounds_bottomright = [1500, 175]

max_mv = [0, 0]

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
      if not (mv[9] == 4):  #  seems like the subpixel resolution is fixed at 1/4 or whatever
         print("motion_scale != 4")

      # alright if we managed to survive the gauntlet let's do this.
      mv_cnt += 1

      # mv indices
      src_x = 3
      src_y = 4
      dst_x = 5
      dst_y = 6
      motion_x = 7
      motion_y = 8

      # Sadly I don't know where origin is and these graphics guys always gotta fuck shit up
      if (mv[src_x] >= bounds_topleft[0]) and (mv[src_x] <= bounds_bottomright[0]) and \
         (mv[dst_x] >= bounds_topleft[0]) and (mv[dst_x] <= bounds_bottomright[0]) and \
         (mv[src_y] >= bounds_topleft[1]) and (mv[src_y] <= bounds_bottomright[1]):

         sum[0] += mv[motion_x]
         sum[1] += mv[motion_y]

   if (mv_cnt):
      #  should probably have an upper bounds too unless turbo doge vtec kicked in yo
      if (sum[0] > 1000):
         print("frame %6d: mv_cnt %d vector sum (%d, %d)" % (frame, mv_cnt, sum[0], sum[1]))
      if sum[0] > max_mv[0]:
         #  DGAF about Y right now
         max_mv[0] = sum[0]  #  a new record!
         #print("frame %6d max_mv x: %d" % (frame, max_mv[0]))


