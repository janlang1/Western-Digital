import csv
import sys

with open(sys.argv[2], 'wb') as csvfile:
    iops_writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    with open(sys.argv[1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        dictionary_of_QOS = {}
        result_dictionary_of_QOS = []
        
        ############# reading from csv #####################
        for row in csv_reader:
            if line_count == 0:
                print 'Columns:', ", ".join(row)

            elif row[3] == "Host command reception by HNVMe":
                dictionary_of_QOS[row[4][10:15]] = [row] #cmd index and timestamp

            elif row[3] == "Command Comletion":
                cmd_index = row[4][9:14]
                if cmd_index in dictionary_of_QOS:
                    dictionary_of_QOS[cmd_index].append(row)
                    dictionary_of_QOS.pop(cmd_index)
                    result_dictionary_of_QOS.append((cmd_index,0))
                

            # elif row[3] == "Command Comletion": break;
            line_count += 1
            
        print "Number of Events Processed:", line_count - 1

        print "Number of Results:" , result_dictionary_of_QOS

