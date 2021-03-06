"""
Aadith PM - COSC 6344 - Visualisation

Script to read two files: a shapefile of linestrings and a CSV file of edges and generate two CSV files with the original edge data and additional attributes for visualization (In this case, road type and classification); the smaller one is a subset for testing. More importantly, it generates two JSON files with an appropriate structure for network visualization with D3; one for testing and the other the whole dataset.

This script is made for datafiles generated with the CSUN (UIC) lab's GISF2E tool.
https://csun.uic.edu/codes/GISF2E.html

I don't use any code from their tool but this project has been made possible thanks to their work with generating clean network representations from data made for GIS and providing access to said data.  
"""

# Fiona for reading shape files, nx for testing the graph, CSV for reading and writing CSV files
# JSON for dealing with JSON files, time for timing script, matplot for the networkx graph
import fiona
import networkx as nx
import csv
import json
import time
import matplotlib.pyplot as plt

# Filenames; change here for different data
shp_filenames = ["Delhi/Delhi_Links.shp", "Houston/Houston_Links.shp", "Chengdu/Chengdu_Links.shp"]
csv_infilenames = ["Delhi/Delhi_Edgelist.csv", "Houston/Houston_Edgelist.csv", "Chengdu/Chengdu_Edgelist.csv"]
csv_outfilenames = ["out_csv/Delhi_Edgelist_Updated.csv", "out_csv/Houston_Edgelist_Updated.csv", "out_csv/Chengdu_Edgelist_Updated.csv"]
csv_testfilenames = ["test_csv/Delhi_Edgelist_Test.csv", "test_csv/Houston_Edgelist_Test.csv", "test_csv/Chengdu_Edgelist_Updated.csv"]
json_filenames = ["json/Delhi.json", "json/Houston.json", "json/Chengdu.json"]
json_testfilenames = ["json_test/Delhi_Test.json", "json_test/Houston_Test.json", "json_test/Chengdu_Test.json"]

log = 1                         # Set this to 1 for logs else 0
test_data_size = 2500           # Change this and comment input line (in main) for setting test dataset size
start_time = time.time()        # For timing the script

def make_json_data(in_file, out_file):
    """
    Takes an input 'in_file' of data in CSV form. Extracts features and stores in JSON 'out_file' with appropriate structure for using in D3 and networkx. 
    """
    data = {}
    data_list = []
    data['directed'] = True
    data['multigraph'] = False
    data['graph'] = {}
    data['nodes'] = []
    data['links'] = []

    reader = csv.reader(open(in_file, 'r'))
    next(reader)

    for entry in reader:
        if entry:
            data_list.append(entry)

    nodes = []
    for entry in data_list:
        id = int(entry[2])
        if id not in nodes:
            nodes.append(id)
        id = int(entry[3])
        if id not in nodes:
            nodes.append(id)

    if log: print("[json] Stored {} nodes".format(len(nodes)))

    nodes = sorted(list(set(nodes)))
    for node in nodes:
        temp_dict = {}
        temp_dict['id'] = node
        data['nodes'].append(temp_dict)

    for entry in data_list:
        data['links'].append(make_edge_data(entry))
    if log: print("[json] Stored {} edges".format(len(data['links'])))

    f = open(out_file, "w")
    json.dump(data, f)


def make_edge_data(entry):
    """
    Takes an input of a list with data elements and builds a JSON entry with appropriate structure for using in D3 and networkx.
    """
    temp_dict = {}
    temp_dict['eid'] = int(entry[4])
    temp_dict['xcoord'] = float(entry[0])
    temp_dict['ycoord'] = float(entry[1])
    temp_dict['source'] = int(entry[2])
    temp_dict['target'] = int(entry[3])
    temp_dict['weight'] = float(entry[5])
    temp_dict['class'] = entry[6]
    temp_dict['type'] = entry[7]
    temp_dict['name'] = entry[8]

    return temp_dict

def build_road_class(shp_list):
    """
    Takes an input of data in a list and returns a dictionary with values of road class for each unique entry
    """
    dict_roadtypes = {}
    for entry in shp_list:
        if entry['properties']['OBJECTID'] not in dict_roadtypes:
            dict_roadtypes[entry['properties']['OBJECTID']] = entry['properties']['type']
    if log: print("[debug] Read {} edges for road classification".format(len(dict_roadtypes)))
    return dict_roadtypes

def build_road_type(shp_list):
    """
    Takes an input of data in a list and returns a dictionary with values of road type for each unique entry
    """
    dict_roadconst = {}
    for entry in shp_list:
        if entry['properties']['OBJECTID'] not in dict_roadconst:
            if entry['properties']['oneway'] == 1:
                dict_roadconst[entry['properties']['OBJECTID']] = "oneway"

            elif entry['properties']['bridge'] == 1:
                dict_roadconst[entry['properties']['OBJECTID']] = "bridge"

            elif entry['properties']['tunnel'] == 1:
                dict_roadconst[entry['properties']['OBJECTID']] = "tunnel"

            else:
                dict_roadconst[entry['properties']['OBJECTID']] = "standard"
    if log: print("[debug] Read {} edges for road type".format(len(dict_roadconst)))
    return dict_roadconst

def build_road_name(shp_list):
    """
    Takes an input of data in a list and returns a dictionary with values of street name for each unique entry
    """
    dict_roadnames = {}
    for entry in shp_list:
        if entry['properties']['OBJECTID'] not in dict_roadnames:
            if entry['properties']['name'] != "" and "?" not in entry['properties']['name']:
                dict_roadnames[entry['properties']['OBJECTID']] = entry['properties']['name']
            else:
                dict_roadnames[entry['properties']['OBJECTID']] = "NULL"

    if log: print("[debug] Read {} edges for road names".format(len(dict_roadnames)))
    return dict_roadnames

def run_script(choice):
    """
    Primary function that extracts data from relevant dataset(s) and generates CSV and JSON files
    """
    files_idx = choice - 1
    shp_filename = shp_filenames[files_idx]
    csv_infilename = csv_infilenames[files_idx]
    csv_outfilename = csv_outfilenames[files_idx]
    csv_testfilename = csv_testfilenames[files_idx]
    json_testfilename = json_testfilenames[files_idx]
    json_filename = json_filenames[files_idx]

    print("\n\nOutputs:\nUpdated CSV: {}\nJSON test file: {}\nFull JSON file: {}\n".
    format(csv_outfilename, json_testfilename, json_filename))

    #
    shp_file = fiona.open(shp_filename)
    csv_file = csv.reader(open(csv_infilename, "r"))
    out_file = open(csv_outfilename, "w")
    out_test_file = open(csv_testfilename, "w")

    #
    dict_roadtypes = {}
    dict_roadconst = {}
    dict_roadnames = {}
    out_list = []

    # Convert file contents from iterator to list for easy access
    shp_list = list(shp_file)
    if log: print("[fiona] Read {} entries from shape file".format(len(shp_list)))

    # Storing road classifications
    dict_roadtypes = build_road_class(shp_list)
    # Storing road types
    dict_roadconst = build_road_type(shp_list)
    # Storing road names
    dict_roadnames = build_road_name(shp_list)

    # Adding headers
    out_list.append(next(csv_file))
    out_list[0].append('CLASS')
    out_list[0].append('TYPE')
    out_list[0].append('NAME')
    
    # Building list for new dataset
    for row in csv_file:
        object_id = int(row[4])     #Index depends on dataset schema
        out_entry = []
        out_entry.extend(row)

        if object_id in dict_roadtypes:
            out_entry.append(dict_roadtypes[object_id])

        if object_id in dict_roadconst:
            out_entry.append(dict_roadconst[object_id])

        if object_id in dict_roadnames:
            out_entry.append(dict_roadnames[object_id])

        out_list.append(out_entry)
    if log: print("[csv] Read and updated {} rows from datafile '{}'".format(len(out_list), csv_infilename))  

    # Saving updated dataset 
    writer = csv.writer(out_file)
    writer.writerows(out_list)
    out_file.flush()
    out_file.close()
    if log: print("[csv] Created complete updated dataset")

    # Saving test dataset
    writer = csv.writer(out_test_file)
    writer.writerows(out_list[:test_data_size])
    out_test_file.flush()
    out_test_file.close()
    if log: print("[csv] Created test dataset")

    # Making JSON files
    make_json_data(csv_testfilename, json_testfilename)
    if log: print("[json] Created test JSON file")

    #make_json_data(csv_outfilename, json_filename)
    #if log: print("[json] Created complete JSON file")

    # Loading data from JSON into a graph and visualizing
    # G = nx.node_link_graph(json.load(open(json_testfilename, "r")))


    # g_pos = nx.spring_layout(G)
    # g_edge_labels = nx.get_edge_attributes(G, 'class')
    # nx.draw(G, pos = g_pos, node_size = 17)
    # nx.draw_networkx_edge_labels(G, pos = g_pos, edge_labels = g_edge_labels, font_size = 7)

    end_time = time.time()
    final_time = end_time - start_time
    if log: print("[debug] Runtime: %.2f seconds" % final_time)

    #plt.show()
    #if log: print("[networkx] Generated graph with {} nodes and {} edges".format(len(G.nodes()), len(G.edges())))



print("--- JSON and CSV file generator for the Force Directed Road Network project ---")
print("--- Choose datafile: 1. Delhi | 2. Houston | 3. Chengdu | 4. All")
while 1:
    choice = input()
    try:
        choice = int(choice)
        print("--- Enter edges limit for test dataset (1000 recommended):")
        test_data_size = int(input())
        if choice in range(1, 4):
            run_script(choice)
            break
        elif choice == 4:
            for i in range(1, 4):
                run_script(i)
            break
        else:
            print("(I) Invalid --- Choose datafile: 1. Delhi | 2. Houston | 3. Chengdu | 4. All")
    except Exception as e:
        print(e)
        print("(E) Invalid --- Choose datafile: 1. Delhi | 2. Houston | 3. Chengdu | 4. All")