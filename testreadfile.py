
from config import *

'''
json test
'''








logs_path =  PATH_CONFIG + PATH_LOGS

file_name = "640ee7878f44427b012eabb7" 

log_fname = logs_path + file_name + ".log"


# file = open(log_fname, "r")
# for count1, line in enumerate(file):
#         pass

# print('Total Lines', count1 + 1)


# file.close()
''''
end count line

'''

# with open(log_fname) as f:
#     lines_after_17 = f.readlines()[5:]

str_logs = []
with open(log_fname) as f:
    for _ in range(5):
        next(f)
    for line in f:
        str_logs.append(line)
print("".join(str_logs))
# fb = open(log_fname, "r")
# lines = fb.readlines()[1:]

# for line in lines:
#     print(line.rstrip())

# while True:
#     line = lines.rstrip()
#     if not line:
#         break
#     print("{}".format(line.strip()))
# count = 0

# for _ in range(5):
#         next(fb)

# for line in fb:
#     line = fb.readline()
#     print(line.strip())
# while True:
#     count += 1
#     if(count < 5): 
#          next(fb)
#     line = fb.readline()

#     if not line:
#         break
#     print("Line{}: {}".format(count, line.strip()))
# fb.close()

# print(line_count)