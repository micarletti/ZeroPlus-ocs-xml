import os

class DatamodelUI:
    def __init__(self):
        self.database_folder = 'database'
        self.selected_database_folder = None
        pass

    def select_database_version(self):
        
        available_database_versions = os.listdir(self.database_folder)
        print('Available datamodel versions:\n')
        for item in enumerate(available_database_versions):
            print(f"{item[0]}) v{item[1]}")

        selection = int(input('\nSelect the number corresponding to your choice: '))
        
        if selection < 0 or selection >= len(available_database_versions):
            print('Invalid selection. Exiting.')
            return

        self.selected_database_folder = available_database_versions[selection]

    def get_database_file(self):
        
        if self.selected_database_folder is None:
            print('No database version selected.')
            return None
        
        return f"{self.database_folder}/{self.selected_database_folder}/datamodel_v{self.selected_database_folder}.db"
    
    def get_database_version(self):
        return self.selected_database_folder
