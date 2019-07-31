# Western-Digital
Java plugin for linking and analyzing data in real time
python scripts for parsing data

data consisted of Print-Statements that a Storage Device generated (like a SSD), that Firmware Engineers used to debug. Then using different data structures (lists, dictionaries, and maps) to link the important data the engineer can use to a readable CSV file, improving debugging efficiency.

METHODOLGY (Java Plugin):
1. Initalize all data structures needed to link events
2. Read in configuration file, basically what the engineer wants to see in the end
3. Read in the data from the test line by line, applying my logic/algorithm to link the lines
4. Dump the data into a csv file that the Engineer can later use to debug the device
