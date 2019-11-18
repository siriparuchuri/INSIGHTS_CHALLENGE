import datetime
import math
from collections import OrderedDict
from datetime import datetime


class Border_analytics:
    report_dict = dict()

    def sum_items(self):
        """
        Sum all the values obtained from the ports and store it in the attribute dictionary for each border, measure
        pair.
        :return: None
        """
        print('Summing the items Initiated')
        for timestamp, border_measures in self.report_dict.items():
            for border_measure, attributes in border_measures.items():
                attributes['sum'] = 0
                for item in attributes['val_list']:
                    attributes['sum'] += int(item)

    def compute_average(self):
        """
        Compute the running monthly average of total crossings for a border and means of crossing across all the months.
        :return: None
        """
        self.report_dict = OrderedDict(sorted(self.report_dict.items(), key=lambda x: x[0], reverse=True))
        date_list = list(self.report_dict.keys())[::-1]

        print('Calculating the running total Initiated')
        running_total_dict = dict()
        for date in date_list:
            for border_measure, attributes in self.report_dict[date].items():
                if border_measure not in running_total_dict:
                    running_total_dict[border_measure] = [attributes['sum'], 1]
                    self.report_dict[date][border_measure]['running_total'] = 0
                else:
                    calcul = running_total_dict[border_measure][0] / running_total_dict[border_measure][1]
                    self.report_dict[date][border_measure]['running_total'] = math.ceil(calcul) if (float(
                        calcul) % 1) >= 0.5 else round(calcul)
                    running_total_dict[border_measure][0] += attributes['sum']
                    running_total_dict[border_measure][1] += 1

    def sort_items(self):
        """
        Sort all the items in the dictionary in descending order by Date, Value or number of crossings, Measure and
        Border.
        :return: None
        """
        print('Sorting items')
        for timestamp, border_measures in self.report_dict.items():
            new_border_measures = OrderedDict(sorted(border_measures.items(),
                                                     key=lambda x: [x[1]['sum'], x[0][1], x[0][0]],
                                                     reverse=True)
                                              )
            self.report_dict[timestamp] = new_border_measures

    def write_to_file(self):
        """
        Write to the output report.csv file with its respective columns Border, Date, Measure, Value and Average.
         :return: None
        """
        print('Writing to a file')
        file_out = open('../output/report.csv', 'w')
        file_out.write('Border,Date,Measure,Value,Average\n')
        for timestamp, border_measures in self.report_dict.items():
            for border_measure, attributes in border_measures.items():
                file_out.write(border_measure[0] + ',')
                file_out.write(timestamp.strftime("%d/%m/%Y %I:%M:%S %p") + ',')
                file_out.write(str(border_measure[1]) + ',')
                file_out.write(str(attributes['sum']) + ',')
                file_out.write(str(attributes['running_total']))
                file_out.write('\n')

    def driver(self):
        """
        The driver code to read the input lines and store them in a dictionary with key as the timestamp and value as a
        border-measures dictionary. Each border-measures dictionary in turn has its respective sum and average values
        for its border and measure attributes. After performing the sum, computing the average and sorting in the
        required order, the contents of the dictionary are written to a file.
        :return:
        """
        counter = 0
        with open('../input/Border_Crossing_Entry_Data.csv', mode='r') as entry_data:
            for line in entry_data:
                if counter == 0:
                    counter += 1
                    continue
                port_name, state, port_code, border, date, measure, value, location = line.split(',')
                timestamp = datetime.strptime(date, "%d/%m/%Y %I:%M:%S %p")
                border_measure = (border, measure)
                if timestamp not in self.report_dict:
                    self.report_dict[timestamp] = dict()
                if border_measure not in self.report_dict[timestamp]:
                    self.report_dict[timestamp][border_measure] = dict()
                    self.report_dict[timestamp][border_measure]['val_list'] = []
                self.report_dict[timestamp][border_measure]['val_list'].append(value)
                counter += 1
                if counter % 100000 == 0:
                    print(counter)
        self.sum_items()
        self.compute_average()
        self.sort_items()
        self.write_to_file()


analysis = Border_analytics()
analysis.driver()
