from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from datamodel_database_module import DatabaseManager

class DatamodelRender:
    """
    This class is responsible for rendering the Modbus configuration file
    using Jinja2 templates based on the datamodel structure.
    """
    def __init__(self, database, database_version, template_dir='templates'):
        """
        Initializes the renderer with the path to the templates directory.

        Args:
            template_dir (str): The directory where the Jinja2 templates are located.
        """
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.config_template = self.env.get_template('Modbus_Config.c.j2')
        self.ocs_template = self.env.get_template('OCS.xml.j2')
        self.db = DatabaseManager(database, database_version)

    def render_config(self):
        """
        Renders the Modbus configuration file from the datamodel dictionary.

        Returns:
            str: The rendered configuration file content.
        """

        database_version = self.db.database_get_version()

        data = {
            'version': database_version['Version'],
            'revision': database_version['Revision'],
            'date': str(datetime.now().strftime("%d-%m-%Y")),
            'rawBufferSize': self.db.database_get_rawbuffer_size(),
            'rawBufferName': 'modbusRegBuffer',
            'databaseName': 'modbusDatabase',
            'blockCount': len(self.db.database_get_block_list()),
            'blockListName': 'modbus_blocks',
            'blockList': self.db.database_get_block_list(),
        }

        return self.config_template.render(data)
    
    def render_ocs(self):
        """
        Renders the OCS XML file from the datamodel dictionary.

        Args:
            datamodel_dict (dict): The datamodel dictionary containing blocks and sections.

        Returns:
            str: The rendered OCS XML content.
        """

        data = {
            'date': datetime.now().strftime("%d/%m/%Y"),
            'xmlRevision': "1",
            'blockList': self.db.database_get_block_list(),
            'referenceList': self.db.database_get_reference_list(),
        }

        return self.ocs_template.render(data)