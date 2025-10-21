import sys
import os

sys.path.append('modules')

from modules.datamodel_render_module import DatamodelRender
from modules.datamodel_ui_module import DatamodelUI

ui = DatamodelUI()
ui.select_database_version()
database_file = ui.get_database_file()
database_version = ui.get_database_version()

if database_file is not None:
    renderer = DatamodelRender(database_file, database_version)

    ocs_xml = renderer.render_ocs()
    modbus_config = renderer.render_config()

    if not os.path.exists('output'):
        os.mkdir('output')

    with open('output/Kalpa_ZERO_XXXX.xml', 'w') as f:
        f.write(ocs_xml)

    with open('output/Modbus_Config.c', 'w') as f:
        f.write(modbus_config)


