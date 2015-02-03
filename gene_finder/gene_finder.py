# -*- coding: utf-8 -*-
"""
Created on Wed Jan  28 3:32:00 2015

@author: Kevin Crispie

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

def flatten(l):
    """ flattens a list of lists
    """
    out = []
    for item in l:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###

def reverse_string(s):
    if len(s) <= 1:
        return s

    return reverse_string(s[1:]) + s[0]
    
def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    """
    if nucleotide=='A':
        complement='T'
    elif nucleotide=='C':
        complement='G'
    elif nucleotide=='T':
        complement='A'
    elif nucleotide=='G':
        complement='C'

    return complement

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    complements = ['b'] * len(dna)
    for x in range (len(dna)):
        complements[x]=get_complement(dna[x])

    complements = ''.join(complements)
    #return complements
    reverse=reverse_string(complements)
    return reverse


def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    """

    """ this program still has the problem that if the first instance of the 
    stop codon is not divisible by 3, then it messes up.
    Right now, it returns dna

    EDIT: This new version considers this possibility
    
    """ 

    for x in range(0,len(dna),3): 
        if dna[x:x+3] == 'TAG' or dna[x:x+3] == 'TAA' or dna[x:x+3] == 'TGA':
            rest_ORF = dna[:x]
            return rest_ORF
        
    return dna


def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    """
    
    frames=[]
    i = 0
    while i < len(dna):
        if dna[i:i+3] == 'ATG':
            frames.append(rest_of_ORF(dna[i:]))
            i += len(rest_of_ORF(dna[i:])) + 3
        else:
            i += 3  
    return frames


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
# runs from 3 different starting positions

    frames1 = find_all_ORFs_oneframe(dna)
    frames2 = find_all_ORFs_oneframe(dna[1:])
    frames3 = find_all_ORFs_oneframe(dna[2:])

    all_frames = frames1 + frames2 + frames3 # puts all frames in list
    return all_frames

"""
    start_indices = [i for i in range(len(dna)) if dna.startswith('ATG',i)]
    all_frames=[]
    #print start_indices
    for x in range(0,len(start_indices)):

        mod_dna=dna[start_indices[x]:]
        #print x
        #print mod_dna
        all_frames.append(find_all_ORFs_oneframe(mod_dna))
    
    #all_frames=sum(all_frames,[]) #may need to change this later
    all_frames=flatten(all_frames)
    return all_frames
"""
def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands. Basically runs find_all_ORFs for both strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """

    dna_comp = get_reverse_complement(dna)
    strand1 = dna
    strand2 = dna_comp

    frames_strand1 = find_all_ORFs(strand1)
    frames_strand2 = find_all_ORFs(strand2)


    both_strand_frames = [frames_strand1, frames_strand2]
    both_strand_frames = sum(both_strand_frames,[])
    return both_strand_frames
    


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """

    all_frames = find_all_ORFs_both_strands(dna)
    longest = max(all_frames, key = len)
    return longest



def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    # TODO: implement this
    pass

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    # TODO: implement this
    pass

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    # TODO: implement this
    pass

if __name__ == "__main__":
    #get_complement('A')
    #get_complement('T')
    import doctest
    doctest.testmod()