import os
from datetime import date
a=date.today()
my_date=a.strftime('%y-%m-%d')
#cmd = "grep {0} logs/5899* | grep Error".format(date)
cmd = "grep Error logs/5899* | grep -v 'properly configured to use 'conda activate'"
#os.path.
print("My command: ", cmd)
os.system(cmd)
#os.system("grep $(date +"+date+")|Error logs/5899* | grep -v 'properly configured to use 'conda activate''")
date.today()
