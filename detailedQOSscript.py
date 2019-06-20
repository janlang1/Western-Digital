import csv
import sys

# if len(sys.argv) < 3: 
#     print "Not enough inputs"
#     sys.exit()

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    dictionary_of_QOS = {}
    result_dictionary_of_QOS = []
    
    ############# reading from csv #####################
    for row in csv_reader:
        if line_count == 0:
            print 'Columns:', ", ".join(row)
            line_count += 1

        elif row[3] == "Host command reception by HNVMe":
            number_of_reception += 1
            line_count += 1
            dictionary_of_QOS[row[4][10:15]] = int(row[0])

        elif row[3] == "Command Comletion":
            number_of_completion += 1
            line_count += 1
            cmd_index = row[4][9:14]
            if cmd_index in dictionary_of_QOS:
                delta = int(row[0]) - dictionary_of_QOS.pop(cmd_index)
                result_dictionary_of_QOS.append((cmd_index, delta))
        
    print "Number of reception:", number_of_reception
    print "Number of completion:", number_of_completion
    print "Number of Events Processed:", line_count - 1
    print "Number of Results:" , len(result_dictionary_of_QOS)
    #print result_dictionary_of_QOS

    ############## writes to new csv file (need to change file name each time, cant override#######
    # with open(sys.argv[2], 'wb') as csvfile:
    #     iops_writer = csv.writer(csvfile, delimiter=' ',
    #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     for first, second in result_dictionary_of_QOS:
    #         iops_writer.writerow([first, ",", second])