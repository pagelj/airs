#!/usr/bin/env python2.7

# coding=utf-8

"""
Awesome Information Retrieval System (AIRS)

Contributors: Prajit Dhar, Janis Pagel
University of Stuttgart
Institute for Natural Language Processing
11/05/2016

"""

import sys

texts = ["3624.txt",
"6730.txt",
"3267.txt",
"4908.txt",
"9844.txt",
"3788.txt",
"5009.txt",
"4769.txt",
"3187.txt",
"76.txt",
"8710.txt",
"5460.txt",
"8413.txt",
"1730.txt",
"8541.txt",
"9442.txt",
"6497.txt",
"7191.txt",
"4406.txt",
"3170.txt",
"6258.txt",
"5839.txt",
"639.txt",
"6201.txt",
"9516.txt",
"4444.txt",
"826.txt",
"9122.txt",
"2180.txt",
"6770.txt",
"621.txt",
"9523.txt",
"5376.txt",
"6226.txt",
"177.txt",
"7404.txt"]

def get_annotation(path):

    annotation_dict = {}

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

            continue

        for query_id in range(len(queries)):

            query = queries[query_id]

            if query in annotation_dict:

                annotation_dict[query].append((doc,annotation[query_id]))

            else:

                annotation_dict[query] = [(doc,annotation[query_id])]

    return annotation_dict


def compute_cohens_kappa(annotation1, annotation2):

    """
    Annotator1/Annotator2   1       0

            1               c1      c2      m1

            0               c3      c4      m0

                            n1      n0      n



    p_0 = (overlapping answers)/(total_answers)

    p_e = (n_1/n * m_1/n) + (n_0/n * m_0/n)

    K = (p_0 - p_e ) / (1 - p_e)
    """

    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0

    for query in annotation1:

        print query

        current_anno_1 = annotation1[query]
        current_anno_2 = annotation2[query]

        for doc1 in current_anno_1:

            for doc2 in current_anno_2:

                if doc1[0] == doc2[0]:

                    if doc1[0] in texts:

                        print doc1[0], doc1[1], doc2[1]

                    if doc1[1] == '1' and doc2[1] == '1':

                        c1 += 1

                    elif doc1[1] == '1' and doc2[1] == '0':

                        c2 += 1

                    elif doc1[1] == '0' and doc2[1] == '1':

                        c3 += 1

                    elif doc1[1] == '0' and doc2[1] == '0':

                        c4 += 1

    n1 = float(c1) + c3
    n0 = float(c2) + c4
    m1 = float(c1) + c2
    m0 = float(c3) + c4
    n = float(c1) + c2 + c3 + c4

    p0 = float(c1 + c4) / n

    pe = (n1/n * m1/n) + (n0/n * m0/n)

    K = (p0 - pe ) / (1 - pe)

    return K

def compute_inter_annotator_agreement(path_anno_1, path_anno_2):

    annotation1 = get_annotation(path_anno_1)
    annotation2 = get_annotation(path_anno_2)

    cohens_kappa = compute_cohens_kappa(annotation1, annotation2)

    print "Cohen's Kappa: " + str(cohens_kappa)

def main(main_args):

    args = sys.argv

    if len(args) != 3:

        sys.exit("""Call the script like this: python inter_annotator_agreement.py path/annotation_1 path/annotation_2""")

    path_1 = args[1]
    path_2 = args[2]

    compute_inter_annotator_agreement(path_1,path_2)


if __name__=='__main__':

    main(sys.argv)
