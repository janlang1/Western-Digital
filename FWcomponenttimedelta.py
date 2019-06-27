#FWcomponenttimedelta
import csv
import sys

# if len(sys.argv) < 3: 
#     print "Not enough inputs"
#     sys.exit()

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    with open(sys.argv[2], 'wb') as csvfile:
        iops_writer = csv.writer(csvfile)
        
        iops_writer.writerow(["Cmd Index", "Total Delta", "FE", "FTL", "PS", "HW"])

        line_count = 0
        dictionary_of_FW_deltas = {}
        result_dictionary_of_QOS = []

        curr_cmd_index = ""
        starting_cmd_timestamp = 0
        starting_FE_timestamp = 0
        starting_FTL_timestamp = 0
        starting_PS_timestamp = 0
        starting_HW_timestamp = 0

        ignore_HVMe_flag = False
        ignore_PS_flag = False
        
        ############# reading from csv #####################
        for row in csv_reader:
            #print line_count,  ": ", row[3]
            if line_count == 0:
                print 'Columns:', ", ".join(row)
                line_count += 1
                continue

            ##########skip 0 timestamp, before test#################
            if "Host command reception by HNVMe" in row[3]:
                #print 1
                without_spaces = row[4].strip()
                curr_cmd_index = without_spaces[10:15]
                starting_cmd_timestamp = int(row[0])
                starting_FE_timestamp = int(row[0])
            
            elif "FE: API HA FW Pop" in row[3]:
                #print 2
                dictionary_of_FW_deltas["FE"] = int(row[0]) - starting_FE_timestamp

            elif "FTL: HRF: Start Handle Flow" in row[3]:
                #print 3
                starting_FTL_timestamp = int(row[0])

            elif "FTL: HRF: Finish Handle Flow" in row[3]:
                #print 4
                dictionary_of_FW_deltas["FTL"] = int(row[0]) - starting_FTL_timestamp
            
            elif "Command Comletion" in row[3]:
                #print "done"
                dictionary_of_FW_deltas["HW"] = int(row[0]) - starting_HW_timestamp
                dictionary_of_FW_deltas["CMD"] = int(row[0]) - starting_cmd_timestamp
                # print dictionary_of_FW_deltas
                iops_writer.writerow([curr_cmd_index, dictionary_of_FW_deltas["CMD"], dictionary_of_FW_deltas["FE"],
                                                    dictionary_of_FW_deltas["FTL"], dictionary_of_FW_deltas["PS"],
                                                    dictionary_of_FW_deltas["HW"]])
                
                dictionary_of_FW_deltas.clear()
                ignore_PS_flag = False
                ignore_HVMe_flag = False
                

            if not ignore_PS_flag:
                #print 5
                if "PS: Debug: DGM Submit PS Req" in row[3]:
                    #print 5-1
                    starting_PS_timestamp = int(row[0])
                    ignore_PS_flag = True

            if not ignore_HVMe_flag:
                #print 6
                if "HNVMe descriptor completion" in row[3]:
                    #print 6-1
                    starting_HW_timestamp = int(row[0])
                    dictionary_of_FW_deltas["PS"] = starting_HW_timestamp - starting_PS_timestamp
                    ignore_HVMe_flag = True
        
            line_count += 1

    print "rows procceded ", line_count

        

        