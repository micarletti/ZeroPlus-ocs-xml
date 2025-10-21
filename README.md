# Datamodel generator tool

## Tools included

### datamodel_generator
This is the main tool file. Use this file to generate the modbus configuration and xml file using one of the database version already present.

Simply launch this script and follow the instruction provided.

All files generated are placed in the ___output___ folder.

### datamodel_csv_importer
This is an helper script for generating a new database file.

> Before running this script you must create a folder named with the version (e.g. 2.00) in the ___database___ folder. Inside this new folder place the csv files that contains all data.

Run the script, select the version in the menu (the * inidicate a folder without the database file) and the script will use the csv files to create a new database file.

## Folder structure

This is the general structure:
- _database_ : This folder contains all database files and the csv used to create the relative database file.
- _modules_ : This folder contains all modules used by the _datamodel_generator_ tool.
- _templates_ : This folder contains all template files used during generation.
- _output_ : This is the output folder, here the tool will generate the _Modbus_Config.c_ and _Kalpa_ZERO_XXXX.xml_ files.

#### database folder
This folder is structured as follow:

```
database/
    x.xx/
        Datamodel_Registers_vx.xx.csv
        Datamodel_Sections_vx.xx.csv
        Datamodel_vx.xx.db
```

- _x.xx_ : This is the version folder.
- _Datamodel_Registers_vx.xx.csv_ : This is the csv file that contains all datamodel registers
- _Datamodel_Sections_vx.xx.csv_ : This is the csv file that contains the datamodel sections
- _Datamodel_vx.xx.db_ : This is the datamodel database

#### modules folder
This folder is structured ad follow:

```
modules/
    __init__.py
    datamodel_database_module.py
    datamodel_render_module.py
    datamodel_ui_module.py
```

- _\_\_init\_\_.py_ : This file is required by python to enable the use of the other files in this folder as modules.
- _datamodel_database_module.py_ : This file is the module responsible to interact with the database and make querys.
- _datamodel_render_module.py_ : This file is the module responsible to render the data from the database to the templates, to generate the output files.
- _datamodel_ui_module.py_ : This file is the module responsible to manage the barebone ui.

#### templates folder
This folder is structured ad follow:

```
templates/
    Modbus_Config.c.j2
    OCS.xml.j2
```
- _Modbus_Config.c.j2_ : This is the template file used to generate the datamodel modbus configuration.
- _OCS.xml.j2_ : This is the template file used to generate the xml for the ocs configuration.

## Limitation
>This script will not generate enums or commands for the XML file.
After generation, the XML file need to be edited by hand to write the enums and commands.
The enumIDs can be found in the database.

## Libraries used
This is the list of python libraries that are used in the tool. 

>Please install all missing libraries before use. 

- os
- sys
- datetime
- csv
- splite3
- jinja2