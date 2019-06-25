import csv
import sys
import re

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    #containers
    dictionary_of_QOS = {}
    dictionary_of_FFLBA_to_cmdindex = {}
    dictionary_of_VBA_to_cmdindex = {}
    result_dictionary_of_QOS = []

    cmd_idx_syntax = ["cmd idx", "cmdidx"]
    
    ############# reading from csv #####################
    for row in csv_reader:
        if line_count == 0:
            print 'Columns:', ", ".join(row)

        line_count += 1

        if "Host command reception by HNVMe" in row[3]:
            dictionary_of_QOS[row[4][12:15]] = [row] #cmd index and row

        elif "Command Comletion" in row[3]:
            cmd_index = row[4][11:14]
            if cmd_index in dictionary_of_QOS:
                dictionary_of_QOS[cmd_index].append(row)
                result_dictionary_of_QOS.append((cmd_index,dictionary_of_QOS[cmd_index]))
                dictionary_of_QOS.pop(cmd_index)#pop after so i can still find the cmd index

        #linked between FFLBA and cmd idx
        elif "FTL: HRF: Start Handle Flow" in row[3]:
            cmd_index = row[4][-3:]
            if cmd_index in dictionary_of_QOS:
                fflba = row[4][:10]
                dictionary_of_FFLBA_to_cmdindex[fflba] = cmd_index
                dictionary_of_QOS[cmd_index].append(row)
                continue

        #looking for cmd idx in the name
        for syntax in cmd_idx_syntax:
            if syntax in row[3].lower():
                array_of_parameters_name = row[3][row[3].find("(")+1:row[3].find(")")].lower().split("|")

                array_of_parameters_parameter = row[4].split("|")
                array_of_parameters_parameter = [parameter.strip(' ') for parameter in array_of_parameters_parameter]
                
                #gives index of where the cmd index is to use for the second list
                cmd_index = [indices for indices, param in enumerate(array_of_parameters_name) if syntax in param]
                cmd_index = cmd_index[0]
                cmd_index = array_of_parameters_parameter[cmd_index][-3:] #truncate

                if(cmd_index in dictionary_of_QOS):
                    dictionary_of_QOS[cmd_index].append(row)
                #done
                continue
        
        #looking for FFLBA in the name
        if "FFLBA" in row[3]: 
            array_of_parameters_name = row[3][row[3].find("(")+1:row[3].find(")")].split("|")
            array_of_parameters_parameter = row[4].split("|")
            array_of_parameters_parameter = [parameter.strip(' ') for parameter in array_of_parameters_parameter]
            fflba = [indices for indices, param in enumerate(array_of_parameters_name) if "FFLBA" in param]
            fflba = fflba[0]

            if(fflba in dictionary_of_FFLBA_to_cmdindex):
                if(dictionary_of_FFLBA_to_cmdindex[fflba] in dictionary_of_QOS):
                    dictionary_of_QOS.append(row)
                    continue

    
    print "Number of Events Processed:", line_count - 1
    print dictionary_of_FFLBA_to_cmdindex
    print dictionary_of_QOS
    # print "Number of Results:" , result_dictionary_of_QOS

    ############## writes to new csv file (need to change file name each time, cant override#######
    with open(sys.argv[2], 'wb') as csvfile:
        iops_writer = csv.writer(csvfile, delimiter=' ',
                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for first, second in result_dictionary_of_QOS:
            for events in second:
                iops_writer.writerow([events[0], ",", events[1],",", events[2],",", events[3],",", events[4],",", events[5],",", events[6]])

