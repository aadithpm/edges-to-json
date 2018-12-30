# GISF2E to JSON
An additional script for CSUN's GISF2E tool to convert the generated CSV files into JSON parsable by D3. Used for my project on force-directed graphs. [[link]](https://github.com/aadithpm/force-road)

**Libraries:** 
* [fiona](https://github.com/Toblerity/Fiona) - parsing shapefile data
* [networkx](https://github.com/networkx/networkx) - testing and displaying graph layout
* [matplotlib](https://github.com/matplotlib/matplotlib) - plotting the graph

**Additional Data:**

1. Download data for the city you want (Credits to UIC's CSUN lab) [[link]](https://figshare.com/authors/Urban_Road_Networks/1263210)
2. Store in separate folder of choice;
- I went with shapefiles, CSV files (the edgelist file is what matters) and all relevant files in a folder called "cityname"; **example:** *'Houston'* for the Houston dataset
3. Add parameters to script.py
- shp_filenames = "foldername/cityname_Links.shp"
- csv_infilenames = "foldername/cityname_Edgelist.csv"
- csv_outfilenames = "out_csv/cityname_Edgelist_Updated.csv"
- csv_testfilenames = "test_csv/cityname_Edgelist_Test.csv"
- json_filenames = "json/cityname.json"
- json_testfilenames = "json_test/Delhi_Test.json"
4. Add options to menu in line 243
5. Increase range in line 250

###### A future version of the script will remove all these steps
###### Note: if you don't have fiona or networkx, you can use 'pip install fiona networkx matplotlib' in the terminal

6. Run script.py (Python 3)
```
python script.py
```

**Optional:** Uncomment the code in line 221 to make whole json file (THIS TAKES A LOT OF TIME)

**Optional:** Uncomment networkx code to prototype graph representation

Finally, move the test JSON files or the JSON files to the web project [[link]](https://github.com/aadithpm/force-road) and add those to the *force.js* script. Alternatively, if you're lazy/just want to test it out, hardcode the data source.


***

* Datasets taken from UIC's CSUN lab [[link]](https://csun.uic.edu/datasets.html)  [[download]](https://figshare.com/articles/Urban_Road_Network_Data/2061897)

* Dataset cleaning, preprocessing and slicing done in Python using fiona and networkx. Script on GitHub [[link]](https://github.com/aadithpm/edges-to-json)

* The datasets used were CSV files generated from shapefiles by CSUN's GISF2E tool [[link]](https://github.com/csunlab/GISF2E/tree/master/Python/v1.20)

* D3.js used for the graph layout. Project can be found on my Github [[link]](https://github.com/aadithpm/force-road)

***
Interactive preview with selective data from Houston, Chengdu and Delhi [[link]](https://aadithpm.github.io/force-road/)

**Note:** Page takes a while to load :)
***

Credits to the people at CSUN for the data, the GISF2E tool.

Credits to Mike Bostock and other contributors for D3.js.
