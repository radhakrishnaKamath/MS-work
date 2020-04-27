import pandas as pd
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser()

# Add argument
parser.add_argument('-a1', required=True, help='first keyword')
parser.add_argument('-a2', required=True, help='start count of a1')
parser.add_argument('-a3', required=True, help='end count jof a1')
parser.add_argument('-o', required=True, help='output path')
args = parser.parse_args()

# extract argument value
first_keyword = args.a1
start_a1 = int(args.a3)
end_a1 = int(args.a3)

outputfile = args.o

result = []

columns = ['src_ip','dst_ip','tcp_sport','tcp_dport','udp_sport','udp_dport','proto','size','count','class']

for i in range(start_a1,end_a1+1):
	inputfile = "../../data/csv/" + first_keyword + "_flow" + i + ".csv"
	flows = pd.read_csv(inputfile)
	
	if len(result) == 0:
		result = flows.to_list()
	else:
		for flow in flows:
			flag = 0
			for res in result:
				if flow[0] == res[0]:
					if flow[1] == res[1]:
						if flow[6] == res[6] and res[6] == 6:
							if flow[2] == res[2]:
								if flow[3] == res[3]:
									res[7] = res[7] + flow[7]
									res[8] = res[8] + flow[8]
									flag = 1
								else:
									continue
							else:
								continue
						elif flow[6] == res[6] and res[6] == 17:
							if flow[2] == res[4]:
								if flow[3] == res[5]:
									res[7] = res[7] + flow[7]
									res[8] = res[8] + flow[8]
									flag = 1
								else:
									continue
							else:
								continue
						else:
							continue
					else:
						continue
				else:
					continue
			if flag == 0:
				result.append(flow)
			
# store the features in the dataframe
for i in result:
	dataframe = pd.DataFrame({'src_ip':[i[0]],'dst_ip':[i[1]],'tcp_sport':[i[2]],'tcp_dport':[i[3]],'udp_sport':[i[4]],'udp_dport':[i[5]],'proto':[i[6]],'size':[i[7]],'count':[i[8]],'class':[i[9]]})
	# save the dataframe to the csv file, if not exsit, create one.
	if os.path.exists(outputfile):
		dataframe.to_csv(outputfile,index=False,sep=',',mode='a',columns = columns, header=False)
	else:
		dataframe.to_csv(outputfile,index=False,sep=',',columns = columns)
