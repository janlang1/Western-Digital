import java.util.*;
import java.lang.*;
import java.io.*;
  
public class ConfigFileRWRPlugin
{
    public final String getPluginInvocationHandlerClassName()
    {
        return "com.sandisk.xrwrdecoder.ioengine.PropertiesRWRPluginInvocationHandler";
    }

    private Map<String, ArrayList<String>> startMap = new HashMap<>(); //start events stored here
    private Map<String, String> inbetweenMap = new HashMap<>(); //in between events stored here
    private Map<String, String> endMap = new HashMap<>(); //end events stored here
    private Map<String, String> counterMap = new HashMap<>(); //events that want to be counted
    private Map<String, String> sequentialMap = new HashMap<>(); //events that follow chronologically and not linked
    private Map<String, String> followerToLearderMap = new HashMap<>(); //events that follow sequential events
    private Map<String, String> mapOfLinkingParameterToKey = new HashMap<>(); //links different parameter syntax to a universial key
    private Map<String, String> mapOfLeaderToKeyHex = new HashMap<>(); //used to link sequential/follower to a KeyHexValue for a track #
    private Map<String, Integer> mapOfEventAndCounter = new HashMap<>(); //used to find event and increase counter
    private Map<String, Integer> mapOfHexValueToTrackNumber = new HashMap<>(); //used to link events using similar HexValues
    private Map<Integer, ArrayList<String[]>> mapOfTrackAndSETevents = new HashMap<>(); //used to store SET events from the config file
    private int trackNumber = 0; 
    private int maxResults = 0;
    private int currentResult = 0;
    private List<Long> topResults = new ArrayList<>(); //used to store top time deltas

    static FileWriter fileWriter; //Couldn't initalize FileWriter object outside methods, need to wrap in static
    static {
        try {
            fileWriter = new FileWriter("results.csv"); //name of csv produced - results file
        } catch (final IOException e) {
            throw new ExceptionInInitializerError(e.getMessage());
        }
    }

    public void init(Map<String, String> initArguments)
    {
        //flag to indicate which section of the configuration file the init() is working on
        boolean startflag = false;
		boolean endflag = false;
		boolean inbtwnflag = false;
        boolean counterflag = false;
        boolean sequentialflag = false; String leader = "";

		try{
			File file = new File("C:\\xTools\\Projectpresentation\\configfile.txt"); //file path of configuration file
			BufferedReader br = new BufferedReader(new FileReader(file)); 
			String lineInFile; 
            while ((lineInFile = br.readLine()) != null){ //read file line for line
                lineInFile = lineInFile.trim();
				if (lineInFile.equals("")){
				} else if (lineInFile.equals("start")) {
					startflag = true; endflag = false; inbtwnflag = false; counterflag = false; sequentialflag = false;
				} else if (lineInFile.equals("inbtwn")) {
					startflag = false; endflag = false; inbtwnflag = true; counterflag = false; sequentialflag = false;
				} else if (lineInFile.equals("end")){
					startflag = false; endflag = true; inbtwnflag = false; counterflag = false; sequentialflag = false;
				} else if (lineInFile.equals("counter")){
					startflag = false; endflag = false; inbtwnflag = false; counterflag = true; sequentialflag = false;
                } else if (lineInFile.equals("sequential")){
					startflag = false; endflag = false; inbtwnflag = false; counterflag = false; sequentialflag = true;
                } else if (lineInFile.contains("max results")){
                    startflag = false; endflag = false; inbtwnflag = false; counterflag = false; sequentialflag = false;
                    String[] stringMaxResult = lineInFile.split(":"); //split the line into name and number
                    maxResults = Integer.parseInt(stringMaxResult[1].trim()); //convert number from string to int
				} else if(lineInFile.charAt(0) != '{'){ //ignore any irrelevant line
					//do nothing
                } else {
                    String[] arrayOfPhrases = lineInFile.split(";", -1); //breaking line into array of phrases
                    for(int i = 0; i < arrayOfPhrases.length; i++){
                        arrayOfPhrases[i] = arrayOfPhrases[i].substring(arrayOfPhrases[i].indexOf("{")+1,arrayOfPhrases[i].indexOf("}")); //taking elements within deliminator
                        if(i == 0){
                            if(startflag){
                                startMap.put(arrayOfPhrases[i], new ArrayList<String>()); //putting phrase in respective map
                            } else if (inbtwnflag){
                                inbetweenMap.put(arrayOfPhrases[i], "placeholder"); //putting phrase in respective map
                            } else if (endflag){
                                endMap.put(arrayOfPhrases[i], "placeholder"); //putting phrase in respective map
                            } else if (counterflag){
                                counterMap.put(arrayOfPhrases[i], "placeholder"); //putting phrase in respective map
                            } else if (sequentialflag){
                                //do nothing;
                            }
                        } else {
                            if(sequentialflag){
                                if(arrayOfPhrases[i].equals("leader")){ //leader will be used to map back to original track
                                    leader = arrayOfPhrases[0]; //SET event name;
                                    sequentialMap.put(arrayOfPhrases[0], "placeholder");
                                    continue;
                                } else if(arrayOfPhrases[i].equals("follower")){
                                    followerToLearderMap.put(arrayOfPhrases[0], leader); //follower is mapped to leader
                                    break;
                                }
                            }
                            String[] arrayOfPairs = arrayOfPhrases[i].split(",", -1); //splitting pair into usable elements
                            if(startflag || inbtwnflag || endflag || sequentialflag){
                                mapOfLinkingParameterToKey.put(arrayOfPairs[0].trim(), arrayOfPairs[1].trim()); //putting elements into linking map
                            }
                            if(startflag){
                                startMap.get(arrayOfPhrases[0]).add(arrayOfPairs[0]);  //putting parameter syntax into map
                            } else if (inbtwnflag){
                                inbetweenMap.put(arrayOfPhrases[0], arrayOfPairs[0]);  //putting parameter syntax into map
                            } else if (endflag){
                                endMap.put(arrayOfPhrases[0], arrayOfPairs[0]);  //putting parameter syntax into map
                            } else if (counterflag){
                                counterMap.put(arrayOfPhrases[0], arrayOfPairs[0]);  //putting parameter syntax into map
                            } else if (sequentialflag){
                                sequentialMap.put(arrayOfPhrases[0], arrayOfPairs[0]);
                            } 
                        }                    
                    }
                }
            }
			br.close();
		} catch(IOException e){
			System.out.println(e);
		}

        //display result of init() in the console
        System.out.println("============================================================================================");
        System.out.println("start map");
        System.out.println(startMap);
        System.out.println("inbtwn map");
        System.out.println(inbetweenMap);
        System.out.println("end map");
        System.out.println(endMap);
        System.out.println("counter map");
        System.out.println(counterMap);
        System.out.println("linkparam map");
        System.out.println(mapOfLinkingParameterToKey);
        System.out.println("sequencial map");
        System.out.println(sequentialMap);
        System.out.println(followerToLearderMap);
        System.out.println("============================================================================================");
    }

    //counting number of relevant events 
    private int startcounter = 0;
    private int inbtwncounter = 0;
    private int endcounter = 0;
    private int countercounter = 0;
    private int sequentialcounter = 0;
    
    public String creatingKeyHex(String linkingParameter, String name, String parameters, boolean single){
        String key = "";
        if(single){ //indicates whether we need a unifying key or can use specific parameter syntax (counterMap)
            key = linkingParameter;
        } else {
            key = mapOfLinkingParameterToKey.get(linkingParameter);
        }
        String lowerLinkingParameter = linkingParameter.toLowerCase();
        String[] arrayOfParameters = (name.substring(name.indexOf("(") + 1, name.indexOf(")"))).toLowerCase().split("\\|");
        String[] arrayOfHexValues = parameters.split("\\|"); //splitting SET event name into its parameters into an arry
        int indexOfLink = 0;
        for (int i = 0; i < arrayOfParameters.length; i++) {
            if (arrayOfParameters[i].contains(lowerLinkingParameter)) { //finding specfic parameter name in the array
                indexOfLink = i;
                break;
            }
        }
        if(indexOfLink >= arrayOfHexValues.length) return "";
        String hexValue = arrayOfHexValues[indexOfLink]; //using index found to access hex value
        return key + hexValue; //combining the unifying key and the hexvalue to distinguish between same hex values
    }

    public int addingInfoToTrack(String keyAndHex, Long timestamp, String name){ //finding the right track to hold current SET event
        int track = mapOfHexValueToTrackNumber.get(keyAndHex);  //getting track number
        String[] usefulInfo = new String[]{timestamp.toString(), name, keyAndHex}; //creating array with useful info
        mapOfTrackAndSETevents.get(track).add(usefulInfo);
        return track; //returning track number if useful for next logic (endMap)
    }

    public void execute(
            Long index,
            String dwords,
            Integer episode,
            Long timestamp,
            String source,
            String type,
            String subSource,
            Integer threadId,
            Integer id,
            String name,
            Integer core,
            String parameters,
            Long fileIndex,
            Date globalTimestamp,
            Long linkedIndex)
                    throws Exception
    {
        //System.out.println(startMap.containsKey(name));
        //HashMap<String, ArrayList<String>> map = startMap.containsKey(name) ?  : inbetweenMap;
        if(startMap.containsKey(name)){
            startcounter++;
            for(String linkingParameter : startMap.get(name)) { //going through each parameter we want to link
                String keyAndHex = creatingKeyHex(linkingParameter, name, parameters, false);

                mapOfHexValueToTrackNumber.put(keyAndHex, trackNumber); //mapping keyAndHex to track number
                mapOfTrackAndSETevents.put(trackNumber, new ArrayList<String[]>()); //making track

                addingInfoToTrack(keyAndHex, timestamp, name);
            }
            trackNumber++; //increment track so it is unique because multiple starts can happen
        } else if(inbetweenMap.containsKey(name)) {
            inbtwncounter++;
            String linkingParameter = inbetweenMap.get(name);
            String keyAndHex = creatingKeyHex(linkingParameter, name, parameters, false);

            if (mapOfHexValueToTrackNumber.containsKey(keyAndHex)) { //check if keyHex has been seen before to be able to be linked to start event
                addingInfoToTrack(keyAndHex, timestamp, name);
            }
        } else if(endMap.containsKey(name)) {
            endcounter++;
            String linkingParameter = endMap.get(name);
            String keyAndHex = creatingKeyHex(linkingParameter, name, parameters, false);
            if(keyAndHex == "") return;

            if (mapOfHexValueToTrackNumber.containsKey(keyAndHex)) {
                int track = addingInfoToTrack(keyAndHex, timestamp, name);

                Long timeDelta = timestamp - Long.parseLong(mapOfTrackAndSETevents.get(track).get(0)[0]); //performing time delta logic
                if(currentResult < maxResults){ //if its the first N results add to maxResults automatically
                    topResults.add(timeDelta);
                    currentResult++;
                } else {                    
                    if (currentResult == maxResults) Collections.sort(topResults, Collections.reverseOrder()); //sorting first N results
                    if(timeDelta > topResults.get(maxResults - 1)){ //only care if longer timehas been found
                        topResults.set(maxResults - 1, timeDelta); //replacing Nth index with new result
                        Collections.sort(topResults, Collections.reverseOrder()); //sort to keep order
                        String[] calculatedInfo = new String[]{"Time Delta", timeDelta.toString()}; //putting time result intp track
                        mapOfTrackAndSETevents.get(track).add(calculatedInfo);

                        for (String[] rowData : mapOfTrackAndSETevents.get(track)){ //writing to csv file with collected "useful info" in track`r3
                            fileWriter.append(String.join(",", rowData));
                            fileWriter.append("\n");
                        }
                    }
                }
                
                mapOfTrackAndSETevents.remove(track); //Remove track from data structure to clear up space
                List<String> keysToDelete = new ArrayList<>(); //Removing HexValue to clear up data structure space to maintain better look up times in hashmap
                for (Map.Entry<String, Integer> entry : mapOfHexValueToTrackNumber.entrySet()) {
                    if (entry.getValue().equals(track)) keysToDelete.add(entry.getKey());
                }
                for (String key : keysToDelete) mapOfHexValueToTrackNumber.remove(key);
            }
        } else if(counterMap.containsKey(name)) {
            countercounter++;
            String linkingParameter = counterMap.get(name);
            String keyAndHex = creatingKeyHex(linkingParameter, name, parameters, true);

            if (mapOfEventAndCounter.containsKey(keyAndHex)) { //if event has been found before increment event by 1 
                int eventCounter = mapOfEventAndCounter.get(keyAndHex);
                eventCounter++;
                mapOfEventAndCounter.put(keyAndHex, eventCounter); 
            } else {
                mapOfEventAndCounter.put(keyAndHex, 1); //else add event with start counter 1
            }
        } else if(sequentialMap.containsKey(name)) { //leader logic
            sequentialcounter++;
            String linkingParameter = sequentialMap.get(name); //getting specific parameter name
            String keyAndHex = creatingKeyHex(linkingParameter, name, parameters, false); //creating keyhex
            if (mapOfHexValueToTrackNumber.containsKey(keyAndHex)){ //if its in the map add it to a track
                addingInfoToTrack(keyAndHex, timestamp, name);
            }
            mapOfLeaderToKeyHex.put(name, keyAndHex);
        } else if(followerToLearderMap.containsKey(name)){ //follower logic
            String keyAndHex = mapOfLeaderToKeyHex.get(followerToLearderMap.get(name)); //getting keyHex from the Leader associated to the Follower
            if (mapOfHexValueToTrackNumber.containsKey(keyAndHex))
                addingInfoToTrack(keyAndHex, timestamp, name);
        }
    }
      
    public void destroy()
    {
        //showing number of relevant SET events in the test
        System.out.println("# of starts: " + Integer.toString(startcounter));
        System.out.println("# of inbtwn: " + Integer.toString(inbtwncounter));
        System.out.println("# of ends: " + Integer.toString(endcounter));
        System.out.println("# of counters: " + Integer.toString(countercounter));
        System.out.println("# of sequential events: " + Integer.toString(sequentialcounter) +  "\n");
        try{
            //showing top results from time delta logic
            fileWriter.append("\n");
            fileWriter.append("Time Delta Results: " + "\n");
            for (Long results : topResults) {
                fileWriter.append(results.toString() + "\n");
            }
            //showing amount of a specific event per command
            fileWriter.append("\n");
            fileWriter.append("Counter Map Results: " + "\n");
			for (Map.Entry<String,  Integer> entry : mapOfEventAndCounter.entrySet()) {
                fileWriter.append(entry.getKey() + " " + entry.getValue().toString() + "\n");
			}
            fileWriter.flush();
            fileWriter.close();
        } catch (IOException e){
            System.out.println(e);
        }
    }
}