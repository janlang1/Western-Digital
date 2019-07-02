####################################
#                                  #
#   using whoami for seconds       #
#                                  #
####################################
import csv
import sys

if len(sys.argv) < 3: 
    print "Not enough inputs"
    sys.exit()

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    ############## opening 
    with open(sys.argv[2], 'wb') as csvfile:
        iops_writer = csv.writer(csvfile)

        seconds = 0
        line_count = 0
        event_counter = 0
        
        ############# reading from csv #####################
        for row in csv_reader:
            if line_count == 0:
                print 'Columns:', ", ".join(row)
                line_count += 1

            ########## skip 0 timestamp, before test #################
            elif row[0] == "0":
                if row[3] == "whoami": line_count += 1
                else: continue

            elif row[3] != "whoami":
                event_counter += 1
                line_count += 1

            elif row[3] == "whoami":
                print seconds, " " , event_counter;
                iops_writer.writerow([seconds, event_counter])
                seconds += 1
                event_counter = 0
                line_count += 1
            

    print 'Number of Events Processed:', line_count - 1
