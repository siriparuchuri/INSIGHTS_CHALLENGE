import datetime
import math
from collections import OrderedDict
from datetime import datetime


class Borderanalytics:
    report = dict()

    def sumitems(self):
       
       
        for timestamp, border_measures in self.report.items():
            for border_measure, attributes in border_measures.items():
                attributes['sum'] = 0
                for item in attributes['val_list']:
                    attributes['sum'] += int(item)

    def computeaverage(self):
       
        self.report = OrderedDict(sorted(self.report.items(), key=lambda x: x[0], reverse=True))
        date_lists = list(self.report.keys())[::-1]

       
        running_total = dict()
        for date in date_lists:
            for border_measure, attributes in self.report[date].items():
                if border_measure not in running_total:
                    running_total[border_measure] = [attributes['sum'], 1]
                    self.report[date][border_measure]['running_total'] = 0
                else:
                    calcul = running_total[border_measure][0] / running_total[border_measure][1]
                    self.report[date][border_measure]['running_total'] = math.ceil(calcul) if (float(
                        calcul) % 1) >= 0.5 else round(calcul)
                    running_total[border_measure][0] += attributes['sum']
                    running_total[border_measure][1] += 1

    def sortitems(self):
        
        
        for timestamp, border_measures in self.report.items():
            new_border_measures = OrderedDict(sorted(border_measures.items(),
                                                     key=lambda x: [x[1]['sum'], x[0][1], x[0][0]],
                                                     reverse=True)
                                              )
            self.report[timestamp] = new_border_measures

    def writetofile(self):
        
        
        file_out = open('../output/report.csv', 'w')
        file_out.write('Border,Date,Measure,Value,Average\n')
        for timestamp, border_measures in self.report.items():
            for border_measure, attributes in border_measures.items():
                file_out.write(border_measure[0] + ',')
                file_out.write(timestamp.strftime("%d/%m/%Y %I:%M:%S %p") + ',')
                file_out.write(str(border_measure[1]) + ',')
                file_out.write(str(attributes['sum']) + ',')
                file_out.write(str(attributes['running_total']))
                file_out.write('\n')

    def driver(self):
   
        counter = 0
        with open('../input/Border_Crossing_Entry_Data.csv', mode='r') as entry_data:
            for line in entry_data:
                if counter == 0:
                    counter += 1
                    continue
                port_name, state, port_code, border, date, measure, value, location = line.split(',')
                timestamp = datetime.strptime(date, "%d/%m/%Y %I:%M:%S %p")
                border_measure = (border, measure)
                if timestamp not in self.report:
                    self.report[timestamp] = dict()
                if border_measure not in self.report[timestamp]:
                    self.report[timestamp][border_measure] = dict()
                    self.report[timestamp][border_measure]['val_list'] = []
                self.report[timestamp][border_measure]['val_list'].append(value)
                counter += 1
                if counter % 100000 == 0:
                    print(counter)
        self.sumitems()
        self.computeaverage()
        self.sortitems()
        self.writetofile()


analysis = Borderanalytics()
analysis.driver()
