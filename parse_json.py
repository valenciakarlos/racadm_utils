import json
with open("/home/carlos/test_results/Nov_10_09_14_Affirmed_3Cards_6GTarget_NO_DROPS/resource-server31_netstats.logs") as json_file:
  json_data=json.load(json_file)

# Print the whole thing
#print(json.dumps(json_data,sort_keys=True,indent=2))
# Print key and values
# Keys on the file
print "Keys on the file -----------------------------------------------"
for key,value in json_data.items():
 print key
# Traversing stats list
stats_list=json_data['stats']
print "Keys on the stats -----------------------------------------------"
for stat in stats_list:
 # This stat is a dictionary with a bunch of keys
 for key,value in stat.items():
     print key

print "Ports list on the stats -----------------------------------------------"
TAB=" \t\t "
print "Port"+TAB+"txmbps"+TAB+"rxmbps"
ports=stat['ports']
print "Keys on a port -----------------------------------------------"
port1=ports[0]
for key,value in port1.items():
 print key
print "Stats for ports-----------------------------------------------"
#for port in ports:  # This is a dictionary. 
#  name=port['name']
#  txmbps=str(port['txmbps'])
#  rxmbps=str(port['rxmbps'])
#  print name+TAB+txmbps+TAB+rxmbps
