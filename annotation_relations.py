class Annotations:
    def __init__(self):
        self.type = None
        self.identifier = None
        self.annotator = None
        self.updated = None
        self.text = None

    def annotation_information(self, annotation_dict: dict) -> bool:
        if type(list(annotation_dict.values())[0]) == dict:
            annotation = list(annotation_dict.values())[0]
            infons = annotation['infons']
            self.type = infons['type']
            self.identifier = infons['identifier']
            self.annotator = infons['annotator']
            self.updated = infons['updated_at']
            # Need to also return location of annotation?
            return True
        else:
            return False


class AnnotationSummary:
    def __init__(self, json):
        self.table_annotations = None
        self.json = json
        self.table_relations = None

    def get_table_annotation(self, table_number: int) -> None:
        documents = self.json["documents"]
        self.table_annotations = documents[table_number]["passages"][2]["annotations"]
        self.table_relations = documents[table_number]["passages"][2]["relations"]


