import sqlite3

class DatabaseManager:
    """
    This class is responsible for managing the SQLite datamodel database.
    """
    def __init__(self, database, version):
        self.database_version = version
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = self.database_row_factory
        self.cursor = self.connection.cursor()

    def database_row_factory(self, cursor, row):
        database_dict = {}
        for idx, col in enumerate(cursor.description):
            database_dict[col[0]] = row[idx]
        return database_dict
    
    def database_get_rawbuffer_size(self):
        self.cursor.execute("SELECT SUM(Size) FROM Register_List")
        rows = self.cursor.fetchone()
        return rows['SUM(Size)'] * 2

    def database_get_block_list(self):
        blocklist = []
        global_offset = 0
        self.cursor.execute("SELECT Block, Address FROM Section_List GROUP BY Block ORDER BY MIN(Address) ASC")
        blocks = self.cursor.fetchall()
        for block in blocks:
            self.cursor.execute("SELECT COUNT(Name) FROM Section_List WHERE Block = ?", (block['Block'],))
            count = self.cursor.fetchone()
            self.cursor.execute("SELECT Name, Address FROM Section_List WHERE Block = ? ORDER BY Address ASC", (block['Block'],))
            sections = self.cursor.fetchall()
            block_length = 0
            sectionlist = []
            for section in sections:
                self.cursor.execute("SELECT Name, Size, Offset, MapLen FROM Register_List WHERE Section = ? ORDER BY Offset ASC", (section['Name'],))
                registers = self.cursor.fetchall()
                self.cursor.execute("SELECT COUNT(Name), SUM(Size) FROM Register_List WHERE Section = ? ORDER BY Offset ASC", (section['Name'],))
                section_data = self.cursor.fetchone()
                section['registers'] = registers
                for register in registers:
                    register['global_offset'] = global_offset
                    global_offset += register['Size'] * 2
                section['length'] = section_data['COUNT(Name)']
                section['size'] = section_data['SUM(Size)'] * 2
                section['Address'] = f"0x{section['Address']:04X}"
                block_length += section_data['COUNT(Name)']
                sectionlist.append(section)
            block_item = {'name': block['Block'], 'length': block_length, 'type': 'Data','count': count['COUNT(Name)'], 'address': f"0x{block['Address']:04X}",'sections': sectionlist}
            blocklist.append(block_item)
        return blocklist
    
    def database_get_reference_list(self):
        self.cursor.execute("SELECT Name, Address FROM Section_List ORDER BY Address ASC")
        sections = self.cursor.fetchall()
        referencelist = []
        referenceID = 20000
        for section in sections:
            self.cursor.execute("SELECT * FROM Register_List WHERE Section = ? AND FormatString IS NOT '' ORDER BY Offset ASC", (section['Name'],))
            registers = self.cursor.fetchall()
            for register in registers:
                register['Address'] = f"0x{(section['Address'] + register['Offset']):0{4}X}"
                if register['ReferenceID'] == '':
                    register['ReferenceID'] = referenceID
                    referenceID += 1
                referencelist.append(register)
        return referencelist
    
    def database_get_version(self):
        self.cursor.execute("SELECT Version, Revision FROM Version")
        version = self.cursor.fetchone()
        return version

    def __del__(self):
        self.connection.close()