#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS)

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
Summer Term 16
04/11/2016

"""

import sys

def convert_csv_2_txt(path, filename):

    output_dict = {}
    output = []

    with open(path.strip(),'r') as openf:

        data = openf.read()

    queries = data.split('\n').pop(0).split(',')[1:]

    data_split = data.split('\n')
    data_split.pop(0)

    for line in data_split:

        if line == '':

            continue

        line_split = line.split(',')
        doc = line_split[0]
        annotation = line_split[1:]

        if 'NA' in annotation:

            break

        for query_id in range(len(queries)):

            query = queries[query_id]

            if query in output_dict:

                output_dict[query].append((doc,annotation[query_id]))

            else:

                output_dict[query] = [(doc,annotation[query_id])]

    for query in output_dict:

        output.append(query.strip('"'))

        for annotation in output_dict[query]:

            output.append(str(annotation[0]).strip('"')+','+str(annotation[1]).strip('"'))

        output.append('')

    with open(str(filename),'w') as outf:

        outf.write('\n'.join(output))




def main(main_args):

    args = sys.argv

    if len(args) != 3:

        sys.exit("Use the script as follows: python csv_2_txt.py path/*.csv filename")

    path = args[1]
    filename = args[2]

    convert_csv_2_txt(path, filename)


if __name__=='__main__':

    main(sys.argv)
