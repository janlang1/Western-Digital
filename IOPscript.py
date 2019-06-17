
import csv
import sys

if len(sys.argv) < 3: 
    print "Not enough inputs"
    sys.exit()

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    event_counter = 0
    list_of_iops = []
    temp_timestamp_str = ""
    temp_timestamp_int = 0
    
    ############# reading from csv #####################
    for row in csv_reader:
        if line_count == 0:
            print 'Columns:', ", ".join(row)
            line_count += 1

        ##########skip 0 timestamp, before test#################
        elif row[0] == "0":
            continue

        ######## setting temp time as placeholder, edge case of the first element ##############
        elif line_count == 1:
            if row[0][-4:-2] == "E+": temp_timestamp_str = ""
            if row[0][-4:-2] != "E+": temp_timestamp_int = int(row[0]) / 1000000000
            event_counter += 1
            line_count += 1

        ######## normal excel number ##########################
        elif row[0][-4:-2] != "E+":
            int_time = int(row[0]) / 1000000000
            if (int_time - temp_timestamp_int) == 1:
                 list_of_iops.append(event_counter)
                 event_counter = 0
            temp_timestamp_int = int_time
            line_count += 1
            event_counter += 1
        
        ######### excel scientific notation ###################
        elif row[0][-4:-2] == "E+":
            string_time = row[0][:-4]
            if len(string_time) > 3: seconds = row[0][3]
            else: seconds = 0

            if seconds != temp_timestamp_str:
                 list_of_iops.append(event_counter)
                 event_counter = 0

            temp_timestamp_str = seconds
            line_count += 1
            event_counter += 1
    print 'Number of Events Processed:', line_count - 1

############## writes to new csv file (need to change file name each time, cant override#######
with open(sys.argv[2], 'wb') as csvfile:
    iops_writer = csv.writer(csvfile, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    i = 0
    for iops in list_of_iops:
        iops_writer.writerow([i, ",", iops])
        i += 1


