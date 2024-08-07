# A Migration visualization focussed on affect
A Human Computer Interaction Thesis Project. These information visualizations were used to measure the difference in data interpretation with a neutral and affective design. The data used in the visualizations is highly aggregated and anonymized CDR data. In this repository, you will find one folder called INFOVIS-NEUTRAL, and one folder called INFOVIS-AFFECTIVE. The content of these folders are the same information visualization, but with different styles. 

# Installation Instructions
1. Download Docker Desktop. See https://docs.docker.com/get-docker/ for further instructions.
2. Download the project.
3. Unzip the project.
4. Open either folder INFOVIS-NEUTRAL or INFOVIS-AFFECTIVE in your terminal and type: docker-compose up (this can take a couple of minutes if you do it for the first time)
5. Go to http://localhost:3000 to view the information visualizaiton.

# Screenshot of the neutral design
![image](https://github.com/user-attachments/assets/2bc54acf-5f03-4811-9d75-c90102c0547d)

# Screenshot of the affective design
![image](https://github.com/user-attachments/assets/dee7b975-a526-46d8-bf1e-ff39103b6a4e)



# Features
**Filters The information visualization offers four filters:** <br>
* Filter on flow direction: This filter allows users to specify the direction of migration flows with the options "From" and "To". 
* Filter on origins and destinations: Depending on the selected direction, this filter enables users to choose the specific origin or destination in the format "FROM X to all" or "from all TO X". Due to the numerous options available (61), a search bar is included to enhance the user experience. Users can select only one option at a time from the list, but "All" is also an option, enabling the display of "from all to all" migration flows, thereby showing the entire dataset.
* Filter on people: This filter provides options for different groups: All, Turks, Syrians, Middle-Eastern (except Syria), and Afghan. To ensure a smooth user experience, this filter includes built-inlogic. While users can select multiple options, selecting "All" will automatically deselect other options, as "All and Turks" is redundant. Similarly, if "All" is selected and the user chooses "Syrians," the "All" option will be automatically deselected, assuming the user is now interested in specific groups.
* Filter on time period: The visualization divides time periods into weekly buckets with the options: All, 2023-01, 2023-02, 2023-03, 2023-04, 2023-05, 2023-06, 2023-07. The same logic as the "Filter
on People" applies here, where selecting "All" will automatically deselect specific weeks, and vice versa.

**Zoom** <br>
The Mapbox GL JS library, used to create the flow map, inherently provides an intuitive zoom functionality. However, excessive zooming can lead to disorientation, causing users to lose their sense of location on the map. To mitigate this issue, a "Reset Zoom" button has been implemented. This feature allows users to instantly return to the default zoom level, centering the map on Türkiye. This not only aids users who may feel lost but also enhances efficiency for those who need to quickly reorient themselves.

**Save and compare** <br>
This information visualization provides users with the ability to compare differences on the map between two sets of filters. A small multiples approach has been applied, allowing users to "save" a map configuration directly on the web page. A user saves a map by pressing the button "save and compare" located at the top right of the map. The saved map is then displayed at the bottom of the page in designated spaces, as illustrated in Figure 39. There is capacity for two saved maps. When a new map configuration is saved, the oldest saved map is replaced by the new one, ensuring users can always compare the two most recent configurations.

**Additional information** <br>
Users have the option to add two supplementary information layers to the map: the connectivity of the selected origin/ destination city to other cities in Türkiye via Facebook, and the
number of collapsed buildings due to the February 6th earthquakes per city. The Facebook connection layer can help answer questions such as, "Are people migrating to cities that are socially connected to the origin city?" The collapsed buildings information layer highlights the cities most affected by the earthquakes and tracks how people from these areas migrated afterward. 

**Hover for explanation** <br>
To not overwhelm users, the layout of the information visualization is designed to be as clean as possible. Therefore, some supportive explanations are "hidden" using a hover functionality. When a user hovers over the flows in the flow map, a tooltip displays the details of the flow. For example, hovering over a flow from Istanbul to Ankara would show "Istanbul -> Ankara: 4 people". The origin, destination, and direction of the flow can already be read visually from the flow map, but when there are a lot of flows close together, it is useful to show this annotation. The number does not exactly represent the number of people in the dataset going from Istanbul to Ankara, it shows the number of trips between two cities. For simplicity, this number is labeled as "people" in the user interface. The map also hints at the volume with the thickness of the flow line; the thinner the line, the fewer trips, the thicker the line, the more trips. Similarly, the bar chart shows tooltips when hovering over the bars. The tooltip clarifies the number of trips per nationality in a given week. While this information can be read from the y-axis of the bar chart, the tooltip provides a more user-friendly and error-free experience. Additionally, the tooltip displays the total number of migrants in that week, a piece of information that would otherwise require manual addition by the user. 

The options to add additional information layers have a hoverable information icon (i) next to it. By hovering over the icon, a pop-up is triggered. The pop-up explains what the additional data layers entail.

**Dynamic chart titles** <br>
The title of the flow map changes dynamically based on the filters selected. The main title indicates the origin, destination, direction, and volume of the migration flows. The subtitle specifies which nationalities and weeks are selected in the filters. These titles are designed to help users understand the data they are viewing, which is particularly useful for first-time users who have not yet interacted with the filters. This consideration is crucial for users who may not immediately recognize the map of Türkiye or be familiar with the city names displayed. When utilizing the "save and compare" functionality, these titles are also replicated and shown in the comparison section of the web page. Clear understanding of the displayed information is essential for this feature to be effective and useful.
