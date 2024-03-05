
import sys

def filename2datetime(fn):
    date = fn[-19:-11]
    h = int(fn[-10:-8])
    m = int(fn[-8:-6])
    s = int(fn[-6:-4])
    time = h*3600 + m*60 + s  #  deal with time as seconds since midnight because EZ
    return (date, time)

class ext_filedata:
    def __init__(self, fn):
        self.filename = fn
        (self.date, self.time) = filename2datetime(self.filename)

class stat_data:
    def __init__(self, bounds, average):
        self.bounds = bounds
        self.average = average
        self.files = []  #  might as well

    def contains(self, time):
        return self.bounds[0] <= time <= self.bounds[1]

input_filelist = sys.argv[1:]

stats = dict()
stats["AM"] = stat_data([6*3600, 12*3600], 25128)
stats["PM"] = stat_data([12*3600, 22*3600], 64349)

filelist = []

for f in input_filelist:
    extdata = ext_filedata(f)

    for k in stats.keys():
        if stats[k].contains(extdata.time):
            stats[k].files.append(extdata)


makefile = open("Makefile.targets", "w")
makefile.write("TARGETS=\\\n")

review_vlc = open("review.vlc", "w")
review_txt = open("review.txt", "w")

for k in ["AM", "PM"]:
    stats[k].files.sort(key=lambda x : abs(stats[k].average - x.time))
    #print(k)
    for f in stats[k].files:
        basename = f.filename[:-4]
        makefile.write("%s.mvtxt \\\n" % basename)
        review_vlc.write("%s\n" % f.filename)
        review_txt.write("%s.mvtxt\n" % basename)

makefile.write("\n")
makefile.close()
review_vlc.close()
review_txt.close()

