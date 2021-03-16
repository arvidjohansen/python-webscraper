import time
import datetime
ts = time.time()


st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print (st)

st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
print (st)