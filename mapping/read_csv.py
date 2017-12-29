import csv

filename = 'clinic_data/egdpprac.csv'


class CSV2Dict:

    def __init__(self, csv_filename):
        self.csv_filename = csv_filename

    def get_dict_clinics(self):
        with open(self.csv_filename) as csvfile:
            read_CSV = csv.reader(csvfile, delimiter=',')
            dental_clinics = []
            for row in read_CSV:
                dc = {
                    'dc_file_id': row[0],
                    'dc_name': row[1],
                    'dc_address_line_1': row[4],
                    'dc_address_line_2': row[5],
                    'dc_address_line_3': row[6],
                    'dc_address_line_4': row[7],
                    'dc_address_line_5': row[8],
                    'dc_postcode': row[9],
                    'dc_status_code': row[12],
                    'dc_practice_type': row[13]
                }
                dental_clinics.append(dc)

            return dental_clinics

# csv_dict = CSV2Dict('clinic_data/egdpprac.csv')
# pprint.pprint(csv_dict.get_dict_clinics())
