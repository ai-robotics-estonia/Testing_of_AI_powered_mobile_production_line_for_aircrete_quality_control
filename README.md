# [Testing of digitalisation and machine learning for quality control of mobile aircrete production equipment]

## Summary
| Company Name | [Kodatek](https://kodatek.ee) |
| :--- | :--- |
| Development Team Lead Name            | [Mattias Põldaru](https://www.etis.ee/CV/Mattias_Poldaru/eng/) |
| Development Team Lead E-mail          | [mattias.poldaru@taltech.ee](mailto:mattias.poldaru@taltech.ee) |
| Duration of the Demonstration Project | 07/2024-04/2025 |
| Final Report | [Report.pdf](https://github.com/ai-robotics-estonia/Testing_of_AI_powered_mobile_production_line_for_aircrete_quality_control/blob/main/Report.pdf) |


# Description
## Objectives of the Demonstration Project

The project’s goal was to test and validate the technical capability for the automatic collection and transmission of production process data to the artificial intelligence database in the required format to train the model. Necessary sensors and camera were installed on the mobile production equipment, which sends data to the control module with each production task. As a result of the project, the model and equipment have recorded data from the process for the initial training of machine learning model.


## Activities and Results of the Demonstration Project
### Challenge

Today the operator is controlling the production process manually. Since the properties of foamed concrete is affected by several factors, taking them all into account without a good model is error prone.

Testing in production revealed that quality control relies on having reliable measurement data on important process parameters. Some of the initially chosen methods (such as weighing a line with material) for data gathering did not provide reliable feedback and the plan was revised. Some additional checks were adjusted to catch different error scenarios, which caused problems during testing.

### Data Sources

Data sources used consist of time-series data of machine speeds, power, flow measurement of liquids and fresh mix, logging of compressed air state, measuring temperature of machine and curing environment. 
Laboratory test results for density are linked to relevant production times and the relationship can be established later using timestamped video stream of production area.

### AI Technologies

Linear regression was used to establish solid base model about the process. Since conducting tests using production-scale machine produces about a hundred litres of material per minute, the initial tests were conducted in a non-wasteful manner, using curated tests to find the core relationships of process parameters.

Real production data will continue to be acquired, which enables the model to be regularly updated. For this a script is used to find correlation between any two time series data columns and to prepare statistical summary for analysis together with laboratory data.

### Technological Results

Continuous data logging for motor controller setpoint/present value of speed and power output was tested with checks for out of bounds values.

Temperature and moisture logging of production line and humidity environment was tested.
Video monitoring of production area to identify timestamps of important ranges of time-series data of testing process was tested.

Laboratory samples were tested for the properties important from the building materials perspective.
Initial relationship between raw values and machine output was determined.

An initial model of relation between production parameters and output was tested. Gathering of the process data gives relevant information about the process. Further data acquisition is needed to fine-tune the process parameters and limits.

### Technical Architecture

The following chart illustrates the data acquisition and process control module signal flows.

![graph](https://raw.githubusercontent.com/ai-robotics-estonia/Testing_of_AI_powered_mobile_production_line_for_aircrete_quality_control/refs/heads/main/scheme_outline.svg)
Figure 1.

### User Interface 

The user interface consists of three parts:
- Control system with GUI to control the motors during test production runs and acquire process parameters related to motors.
- Visualization of raw data for both live viewing and later analysis using Grafana dashboards.
- Command line scripts to query the database for statistical profile and correlation analysis of data for chosen data columns and ranges.

### Future Potential of the Technical Solution

The technical solution of data acquisition and process control can be used to improve aircrete production lines. It is very similar to the needs of mortar production lines for concrete 3D printing and probably other production lines with similarly continuous process.

### Lessons Learned

Measuring process data live and setting up error conditions to stop or block starting the system reduces the most apparent possibility of producing non-compliant material.

The initially chosen measurement methods were partly insufficient to provide reliable feedback about the density of the produced material. A Coriolis effect based sensor system was chosen as a replacement for the earlier method.
