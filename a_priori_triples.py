from __future__ import division

import itertools
#from operator import itemgetter

def basket_generator(filename):
    with open(filename, 'r') as f:
        for line in f:
            basket = line.split(' ')
            yield basket

def item_counter(item, count_dict):
    if item in count_dict:
        count_dict[item] += 1
    else:
        count_dict[item] = 1
    return count_dict

def support_filter(count_dict, s):
    freq_dict = {}
    for key in count_dict:
        if key == '\n':
            pass
        elif count_dict[key] >= s:
            freq_dict[key] = count_dict[key]
    return freq_dict

def confidence_score(Iuj_dict, Ij_dict, lines_to_print=-1):
    output = []
    for Iuj in Iuj_dict:
        Is = itertools.combinations(Iuj, len(Iuj)-1)
        for I in Is:
            j = (set(Iuj) - set(I)).pop()
            # get string from I for dict key len(I) = 1
            if len(I) == 1:
                I = I[0]
            # gives float due to division import
            confidence = Iuj_dict[Iuj] / Ij_dict[I]
            # use 1. - confidence for sorting
            output.append((1. - confidence, '{0} -> {1}'.format(I, j)))
    output.sort()
    line_num = 0
    for entry in output:
        line_num += 1
        # print original confidence using 1. - entry[0]
        print '{0} conf = {1}'.format(
                   entry[1], 1. - entry[0])
        if line_num == lines_to_print:
            print '\n'
            break

def get_freq_singles(filename, s):
    singles_count = {}
    for basket in basket_generator(filename):
        for item in basket:
            singles_count = item_counter(item, singles_count)
    freq_singles = support_filter(singles_count, s)
    return freq_singles
    

def pairs_generator(basket, freq_singles):
    # generate all pair combinations in a given basket
    # only if the the singles comprising the pair are
    # frequent
    remaining_singles = [item for item in basket if item in freq_singles]
    # sort ensures we don't have to worry about item order
    # in the pair
    remaining_singles.sort()
    pairs = itertools.combinations(remaining_singles, 2)
    return pairs

def get_freq_pairs(filename, freq_singles, s):
    # gets pairs of items where each item has support s
    # the support of each item is contained in 'freq_singles'
    pairs_count = {}
    for basket in basket_generator(filename):
        pairs = pairs_generator(basket, freq_singles)
        for pair in pairs:
            pairs_count = item_counter(pair, pairs_count)
    freq_pairs = support_filter(pairs_count, s)
    return freq_pairs

def get_freq_triples(filename, freq_pairs, s):
    triples_count = {}
    for basket in basket_generator(filename):
        remaining_pair_singles = []
        basket.sort()
        basket_pairs = itertools.combinations(basket, 2)
        for pair in basket_pairs:
            if pair in freq_pairs:
                for single in pair:
                    if single not in remaining_pair_singles:
                        remaining_pair_singles.append(single)
        remaining_pair_singles.sort()
        triples = itertools.combinations(remaining_pair_singles, 3) 
        for triple in triples:
            triples_count = item_counter(triple, triples_count)
    freq_triples = support_filter(triples_count, s)
    return freq_triples

def print_number(s, item_type, item_number):       
    """
    Args:
        s (int): support value
        item_type (str): type of itemset
        item_number (int): number of items in itemset
    """
    print 'This is the number of {0} with support >= {1}: {2}\n'.format(
           item_type, s, item_number)


def main():
    filename = 'browsing.txt'
    s = 100
    
    print "Pass 1, getting frequent singles"
    freq_singles = get_freq_singles(filename, s)
    print_number(s, 'singles', len(freq_singles))
    
    print "Pass 2, getting frequent pairs"
    freq_pairs = get_freq_pairs(filename, freq_singles, s)
    print_number(s, 'pairs', len(freq_pairs))
    
    print "Pass 3, getting frequent triples"
    freq_triples = get_freq_triples(filename, freq_pairs, s)
    print_number(s, 'triples', len(freq_triples))
    
    print "Top pairs by confidence:\n"
    confidence_score(freq_pairs, freq_singles, lines_to_print=15)
    
    print  "Top triples by confidence:\n"
    confidence_score(freq_triples, freq_pairs, lines_to_print=20)


if __name__ == '__main__':
    main()
