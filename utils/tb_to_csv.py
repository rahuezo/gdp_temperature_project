import tkFileDialog as fd
import csv



def tb_to_csv(tb_file): 
    records = {}

    with open(tb_file, 'rb') as f: 
        reader = csv.reader(f)
        reader.next()

        for row in reader:             
            key = tuple(row[:7])

            if key not in records: 
                records[key] = row + [row[-1]]
            else: 
                records[key][-1] = row[-1]

    # print "Records: ", records

    fout_path = fd.asksaveasfilename(title="Save csv as")

    with open(fout_path, 'wb') as fout: 
        writer = csv.writer(fout, delimiter=',')

        nprints = 0

        print "\nWriting tb to csv"
        for i, record in enumerate(records): 
            if i == 0: 
                print "\t{} out of {} records".format(i + 1, len(records))

            if nprints >= 1000:                 
                print "\t{} out of {} records".format(i + 1, len(records))
                nprints = 0
            else:
                nprints += 1
            
            try: 
                writer.writerow(records[record])
            except Exception as e: 
                print e
                print records[record]
                continue

        print "\nFinished writing tb to csv"
        




f = fd.askopenfilename(title="Choose tree level records csv")

tb_to_csv(f)
