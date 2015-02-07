# -*- coding: utf-8 -*-
"""
Created on Wed Jan  28 3:32:00 2015

@author: Kevin Crispie

"""
#importing functions for later use in program
from amino_acids import aa, codons, aa_table
import random
from load import load_seq
dna = load_seq("./data/X73525.fa")

def shuffle_string(s):
    """ Shuffles the characters in the input string
    """
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

def reverse_string(string):
    """ helper function that revervses a string
    """
    return string[-1:-len(string)-1:-1] #reverse string using Python's negative indexing
    
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
    complements = ['b'] * len(dna) #initializes the complement list
    for x in range (len(dna)):
        complements[x]=get_complement(dna[x]) #populates list with corresponding nucleotide complements

    complements = ''.join(complements) #makes the list into a string
    #return complements
    reverse=reverse_string(complements) #reverses the string to get the reverse complement
    
    return reverse  #returns the reverse complement as a string


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
        possible frames and returns them as a list.  By non-nested I mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it is not be included in the returned list of ORFs.
        
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
        strands. It runs find_all_ORFs for both strands. 
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    # defines each strand of dna
    dna_comp = get_reverse_complement(dna) #defines dna complement
    strand1 = dna     #assigns strand 1 to be the dna
    strand2 = dna_comp #assigns strand 2 to be the dna complement

    frames_strand1 = find_all_ORFs(strand1)
    frames_strand2 = find_all_ORFs(strand2)


    both_strand_frames = [frames_strand1, frames_strand2] #puts all frames into list
    both_strand_frames = sum(both_strand_frames,[]) #makes list of lists into one list
    
    return both_strand_frames  #returns the ORFs from both strands in a list
    


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """

    all_frames = find_all_ORFs_both_strands(dna) #finds all ORFs in dna 

    #deals with the case or empty list, returning a blank if there are no ORFs

    if len(all_frames) > 0:
        longest = max(all_frames, key = len)
    else:
        longest = ''    #returns blank if there are no ORFs in dna
    
    return longest #returns string, the longest ORF in the given dna



def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    
    shuffled_dna = ['s']*num_trials
    longest_ones = ['0']* num_trials

    for x in range(0,num_trials):
        shuffled_dna[x] = shuffle_string(dna)
        longest_ones[x] = longest_ORF(shuffled_dna[x])         

    #deals with the case or empty list

    if len(longest_ones) > 0:
        max_ORF = max(longest_ones, key=len)
    else:
        max_ORF = ''

    max_length = len(max_ORF)  #calculates length of longest ORF through all tests

    return max_length     # returns integer, the length of longest ORF



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

    
    AA_chain = [] #initializes the list of the amino acid chain as an empty list

    # if there are any extra nucleotides, the function removes them, otherwise it uses
    # the entire dna sequence as a coding strand
    
    if len(dna) % 3 != 0:     #cehcks if dna has only triplet codons
        coding_strand = dna[:len(dna)-(len(dna)%3)] #if it doesn't, it removes extra nucleotides
    else:
        coding_strand = dna # if there are no extra nucleotides, the coding strand is dna

    for x in range(0,len(coding_strand),3):
        AA_chain.append(aa_table[dna[x:x+3]]) #uses imported aa_table dictionary to fin amino acid

    return ''.join(AA_chain)  #turns list into a string, returns the string

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    
    thresh = longest_ORF_noncoding(dna,1500) #computes trheshold based on 1500 tests
    
    all_ORFs = find_all_ORFs(dna)  #opens all reading frames
    
    #returns all ORFs above the threshold
    above_thresh = [] #intitializes above_thresh as an empty list
    for x in range(len(all_ORFs)):
        if len(all_ORFs[x])> thresh:
            above_thresh.append(all_ORFs[x])  #poulates list using append function


    #determines amino acids encoded by dna

    amino_acids = []
    
    for x in range(len(above_thresh)):
        amino_acids.append(coding_strand_to_AA(above_thresh[x]))


    return amino_acids   #returns list of amino acids


amino_acids = gene_finder(dna)
print amino_acids

#if __name__ == "__main__":
    #import doctest
    #doctest.testmod()