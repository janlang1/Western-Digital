#configQOSscript
import csv
import sys

starter = {}
ender = {}
keywords = []

def checkCmdArg():
    if len(sys.argv) < 4: 
        print "Need csv and config file"
        sys.exit()

def readConfigFile(filename):
    with open(filename, "r") as txt:
        starter_flag = False
        ender_flag = False
        for row in txt:
            if not row.strip(): continue
            elif "#" in row: continue
            elif "starters" in row: 
                starter_flag = True
                ender_flag = False
                continue
            elif "enders" in row: 
                starter_flag = False
                ender_flag = True
                continue

            row = row.rstrip('\n')
            array_of_key_value = row.split(",")
            array_of_key_value = [value.strip(' ') for value in array_of_key_value]

            if starter_flag:
                keywords.append(array_of_key_value[1])
                starter[array_of_key_value[0]] = array_of_key_value[1] 
            
            elif ender_flag:
                ender[array_of_key_value[0]] = array_of_key_value[1]

def findingKeyInArray(row_array, key):
    name = row_array[3].lower()
    #makes array
    array_of_parameters_name = row_array[3][row_array[3].find("(")+1:row_array[3].find(")")].lower().split("|")
    array_of_parameters_parameter = row_array[4].split("|")
    array_of_parameters_parameter = [parameter.strip(' ') for parameter in array_of_parameters_parameter]
    
    #finds key (in this case cmd index) index  to use for the second list
    key_index = [indices for indices, param in enumerate(array_of_parameters_name) if key in param]
    key_index = key_index[0]
    key_index = array_of_parameters_parameter[key_index]# cant truncate anymore bc we are generalizing the whole thing[-3:] #truncate
    return key_index



link_results = {}          

def main():
    checkCmdArg()
    readConfigFile(sys.argv[1])
    print keywords
    print starter
    print ender
    with open(sys.argv[2]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

        with open(sys.argv[3], 'wb') as csvfile:
            qos_writer = csv.writer(csvfile)
            #qos_writer.writerow()
            for row in csv_reader:
                if row in starter:
                    key = starter[row] #in this case it will be the cmd idx
                    key_index = keyfindingKeyInArray(row, key)
                    link_results[key_index] = [row]
                if row in ender:
                    link_results[row]


if __name__ == "__main__":
    main()

#     mydict = {'george':16,'amber':19}
# print mydict.keys()[mydict.values().index(16)] finding key with value;