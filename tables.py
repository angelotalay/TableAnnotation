import dataclasses
from annotation_relations import Annotations, AnnotationSummary
import json

TEST_FILE = '/home/aagt1/Downloads/TableRender_PHP/JSON/V3/PMC3775874_tables.json'


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

    def all_table_information(self):
        tables = []
        headings = []
        """ Wrapper method that obtains all table information """
        for n in range(len(self.documents)):  # Iterate through all the tables
            self.get_table_data(n)
            headings.append(self.headers)
            table_row_information = self.get_rows()
            tables.append(table_row_information)
        self.headers = headings
        return tables


def unpack_annotation(annotation_dict: dict):
    if type(list(annotation_dict.values())[0]) == dict:
        annotation_cell = list(annotation_dict.values())[0]
        infons = annotation_cell['infons']
        annotation_type = infons['type']
        cell_text = list(annotation_dict.keys())[0]
        if annotation_type == 'significance':
            set_class = 'significance'
        elif annotation_type == 'trait':
            set_class = 'trait'
        else:
            set_class = 'genetic_variant'
        return cell_text, set_class
    elif type(list(annotation_dict.values())[0]) == str:
        cell_text = list(annotation_dict.keys())[0]
        return cell_text, None


if __name__ == "__main__":
    tables = ObtainTables("/home/aagt1/Downloads/TableRender_PHP/JSON/V3/PMC3775874_tables.json")
    tables.load_json()
    tables.table_summary()
    all_tables = tables.all_table_information()
    annot_summary = AnnotationSummary(tables.json)
    for n in range(len(all_tables)):
        annot_summary.get_table_annotation(n)
        print(len(annot_summary.table_annotations))
        if annot_summary.table_annotations:
            annotations_list = annot_summary.table_annotations
            for annotation in annotations_list:
                # print(annotation['text'])
                pass

        else:
            pass

        # for section, rows in all_tables[n].items():
        #     if type(section) == int:
        #         for cells in rows:
        #             row = rows[cells]
        #             for cell in row:
        #                 annotation_class = Annotations
        #                 obtained_annotation = annotation_class.annotation_information(cell)
        #                 print(obtained_annotation)
        #     elif type(section) == str:
        #         for cells in rows:
        #             row = rows[cells]
        #             for cell in row:
        #                 pass