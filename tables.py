import dataclasses
import json

TEST_FILE = '/home/aagt1/PycharmProjects/TableAnnotation/PMC5300750_tables.json'


class ObtainTables:
    def __init__(self, table_path: str):
        self.table_information = None
        self.path_to_table = table_path
        self.json = None
        self.documents = None
        self.headers = None
        self.table_data = None
        self.table_sections = None
        self.all_table_annotations = None
        self.table_annotations = None

    def load_json(self):
        with open(self.path_to_table) as file:
            json_file = json.load(file)

        self.json = json_file
        self.documents = json_file['documents']

    def table_summary(self) -> tuple:
        table_ids = [table['id'] for table in self.documents]
        table_titles = [table['passages'][0]['text'] for table in self.documents]
        table_captions = [table['passages'][1]['text'] for table in self.documents]

        return table_ids, table_titles, table_captions

    def get_table_data(self, table_number: int) -> None:
        """Method that retrieves table data and annotations"""
        # Get table data and store column headings first
        self.table_data = self.documents[table_number]['passages'][2]
        self.headers = self.documents[table_number]['passages'][2]['column_headings']
        self.table_annotations = self.documents[table_number]['passages'][2]['annotations']
        # table_rows = {}
        section_dict = {}

        # Get sections and section titles second
        for num, section in enumerate(self.table_data['data_section']):
            # Check if there is a section title:
            if 'infons' in section:
                infons = section['infons']
                if infons['iao_name_1'] == 'section title':
                    section_dict[section['text']] = section['data_rows']
            else:
                section_dict[num] = section['data_rows']

        self.table_sections = section_dict

    @staticmethod
    def cross_reference(dictionary_list: list, value: dict, annotations: dict):
        """ Method to insert annotation information into cells for table rendering"""
        for item in dictionary_list:
            for k, v in item.items():
                if v == value:
                    item[k] = annotations

    def get_rows(self):
        rows_dict = {}
        for sect, rows in self.table_sections.items():
            sect_rows = {}
            for n in range(len(rows)):
                row = rows[n]
                sect_rows[n] = [{cell['cell_text']: cell['cell_id']} for cell in row]  # Get the cell text and
                # cell_id for each cell in a row
                # cross-reference with annotation cell ids.

                for annotations in self.table_annotations:  # Iterate through the annotations and see if they are
                    # present within a row
                    locations = annotations['locations']
                    for location in locations:
                        location_cell_id = location['cell_id']
                        self.cross_reference(sect_rows[n], location_cell_id, annotations)

            rows_dict[sect] = sect_rows
        return rows_dict


if __name__ == "__main__":
    table = ObtainTables(TEST_FILE)
    table.load_json()
    table.table_summary()
    table.get_table_data(1)
    table_rows = table.get_rows()
    for section, rows in table_rows.items():
        if type(section) == int:
            for cells in rows:
                print(rows[cells])