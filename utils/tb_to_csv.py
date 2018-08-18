import tkFileDialog as fd
import csv



def tb_to_csv(tb_file): 
    records = {}

    with open(tb_file, 'rb') as f: 
        reader = csv.reader(f)
        header = reader.next()
        header[-1] = 'First Tree Year'
        header += ['Last Tree Year']

        for row in reader:             
            key = tuple(row[:7])

            if key not in records: 
                records[key] = row + [None]
            else: 
                records[key][-1] = row[-1]

    print "Records: ", records

    fout_path = fd.asksaveasfilename(title="Save csv as")

    with open(fout_path, 'wb') as fout: 
        writer = csv.writer(fout, delimiter=',')

        writer.writerow(header)

        print "\nWriting tb to csv"
        for i, record in enumerate(records): 
            print "\t{} out of {} records".format(i + 1, len(records))
            writer.writerow(record)

        print "\nFinished writing tb to csv"
        




f = fd.askopenfilename(title="Choose tree level records csv")

tb_to_csv(f)
