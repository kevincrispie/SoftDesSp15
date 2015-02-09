# -*- coding: utf-8 -*-
"""
Created on Wed Jan  28 3:32:00 2015

@author: Kevin Crispie

"""

from amino_acids import aa, codons, aa_table
import random
from load import load_seq


def shuffle_string(s):
    """ Shuffles the characters in the input string

    There are no doctests for this function since it randomly shuffles
    the input string

    """
    
    return ''.join(random.sample(s,len(s)))

def reverse_string(string):
    """ helper function that revervses a string

    Doctest:

    Doctests reverse string regardless of string length or makeup

    >>> reverse_string('AMERICA!')
    '!ACIREMA'
    >>> reverse_string('JOHNNY B. GOODE')
    'EDOOG .B YNNHOJ'
    
    """
    
    return string[::-1] 
    
def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    
    Doctests:

    Orginial and added doctests cover each of the four nucleotide bases

    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    
    Added Doctests:

    >>> get_complement('T')
    'A'
    >>> get_complement('G')
    'C'

    """
    
    if nucleotide == 'A':  
        complement = 'T'
    elif nucleotide == 'C': 
        complement = 'G'
    elif nucleotide == 'T':  
        complement = 'A'
    elif nucleotide == 'G':  
        complement = 'C'

    return complement 

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence.
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    
    Doctests:

    The first two doctests adequately test whether the function both correctly
    determines the complement of the DNA sequence and reverses it. The added 
    doctests makes sure the function works at its most basic level,
    returning a sinlge nucleotide complement if the DNA strand input is only
    one nucleotide long.

    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'

    Added Doctest:

    >>> get_reverse_complement("C")
    'G'

    """
    
    complement = ''
    for x in range (len(dna)):
        complement += get_complement(dna[x]) 

    reverse=reverse_string(complement) 
    
    return reverse  


def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  
        If there is no in frame stop codon, it returns the whole string.
        
        dna: a DNA sequence as a string
        returns: the open reading frame represented as a string
    
    Doctests:

    -The first doctest tests whether the correct ORF will be returned,
    ignoring everything after the stop codon as well as the stop codon itself
    -The second doctest does this as well, but also makes sure iteration will
    be terminated only if the stop codon string is in the correct place, coming
    after an integer number of other codons
    -The third doctest also tests whether the function will ignore the stop 
    codon and all nucleotides after it, but also makes sure that the function
    returns an empty string if it starts with a stop codon

    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    
    Added Doctest:

    >>> rest_of_ORF("TAGG")
    ''

    """

    for x in range(0,len(dna),3): 
        if dna[x:x+3] in ['TAG', 'TAA', 'TGA']:
            rest_ORF = dna[:x]
            return rest_ORF
        
    return dna

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence as a string
        returns: a list of non-nested ORFs
    
    Doctests:

    -The first doctest makes sure that only ORFs that start on indices that
    are multiples of 3 are returned.
    -The second doctest also makes sure that the ORF will only be returned
    if the start codon starts on an indeex multiple of 3. It also ensures 
    that if no valid ORFs are found, an empty list is returned and does not
    produce an error.
    -The third doctest shows that the function does not return nested ORFs.

    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']

    Added Doctests:

    >>> find_all_ORFs_oneframe("CCATGAGGGTAG")
    []

    >>> find_all_ORFs_oneframe("ATGATGTAGTAG")
    ['ATGATG']

    """
    
    frames=[]  
    i = 0  
    while i < len(dna):
        if dna[i:i+3] == 'ATG': 
            frames.append(rest_of_ORF(dna[i:]))
            i += len(rest_of_ORF(dna[i:])) + 3 #increments counter by length of ORF and the stop codon
        else:
            i += 3  #increments counter by 3 if no start codon found to search starting at next codon
    return frames


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested I mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it is not be included in the returned list of ORFs.
        
        dna: a DNA sequence as a string
        returns: a list of non-nested ORFs

    Doctests:

    -The first doctest tests whether the function can correctly parse out
    different ORFs from a single strand.
    -The second doctest ensures that the function returns an empty list
    if there are no valid ORFs and does not produce an error.
    -The third doctest shows that the function does not return nested ORFs.

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']

    Added Doctests:

    >>> find_all_ORFs("AAAAAAAAA")
    []

    >>> find_all_ORFs("ATGATGTAGTAG")
    ['ATGATG']

    """

    frames1 = find_all_ORFs_oneframe(dna)
    frames2 = find_all_ORFs_oneframe(dna[1:])
    frames3 = find_all_ORFs_oneframe(dna[2:])

    all_frames = frames1 + frames2 + frames3 
    
    return all_frames  

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands. It runs find_all_ORFs for both strands. 
        
        dna: a DNA sequence as a string
        returns: a list of non-nested ORFs
    
    Doctests:

    -The first doctest ensures that the correct ORFs for the dna and 
    complement are returned.
    -The second doctest makes sure that the function handles an invalid DNA
    sequence, returning an empty list if the strand does not code for anything
    and does not produce an error.


    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']

    Added Doctest:

    find_all_ORFs_both_strands("AAAAAAAAA")
    []

    """
    
    dna_comp = get_reverse_complement(dna) 

    frames_dna = find_all_ORFs(dna) 
    frames_dna_comp = find_all_ORFs(dna_comp) 

    both_strand_frames = frames_dna + frames_dna_comp 
    
    return both_strand_frames  
    


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA

        dna: a DNA sequence as a string
        returns: the longest ORF as a string

    Doctests:

    -The first doctest ensures that the function interfaces correctly with
    logest_ORF and returns the longest ORF result from that function
    -The second doctest makes sure that the function returns an empty string
    when the input DNA sequence does not code for anything and does not produce
    an error.

    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    
    Added Doctest:

    >>> longest_ORF("AAAAAAAAA")
    ''

    """

    all_frames = find_all_ORFs_both_strands(dna)  

    #deals with the case or empty list, returning a blank if there are no ORFs

    if len(all_frames) > 0:
        longest = max(all_frames, key = len)
    else:
        longest = ''    #returns blank if there are no ORFs in dna
    
    return longest 



def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length of the longest ORF as integer

        There are no doctests for this function because shuffle_string acts
        differently each time it runs.
        """
    
    shuffled_dna = ['s']*num_trials   
    longest_ones = ['0']* num_trials  

    for x in range(0,num_trials):
        longest_ones[x] = longest_ORF(shuffle_string(dna))         

    #deals with the case or empty list

    if len(longest_ones) > 0:
        max_ORF = max(longest_ones, key=len) #as long as list is not empty, determines largest element of list
    else:
        max_ORF = ''      #max_ORF is a blank if the list is empty

    max_length = len(max_ORF)  

    return max_length 



def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region). 
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        Doctests:

        -The first doctest checks to see whether the amino acid assignment
        works as intended.
        -The second doctest makes sure that the function returns the correct
        amino acid sequence with two extra nucleotides in the sequence.
        -The third doctest makes sure that the function returns the correct
        amino acid sequence with one extra nucleotide in the sequence.
        -The fourth doctest makes sure the function returns the correct
        amino acid sequence even though there is no sart codon
        -The fifth doctest makes sure the function returns an empty string
        when there are no complete codons in the dna strand
        -The sixth doctest makes sure that if there is a stop codon in the 
        dna sequence, it will still run, and return a '|' in the place of 
        an amino acid, as it is defined in the aa_table dictionary


        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'

        Added Doctests:

        >>> coding_strand_to_AA("ATGCCCGCTT")
        'MPA'
        >>> coding_strand_to_AA("CGA")
        'R'
        >>> coding_strand_to_AA("CG")
        ''
        >>> coding_strand_to_AA("TAG")
        '|'

    """ 
    
    AA_chain = '' 
    
    if len(dna) % 3 != 0:     #checks if dna has only triplet codons
        coding_strand = dna[:len(dna)-(len(dna)%3)] #if it doesn't, it removes extra nucleotides
    else:
        coding_strand = dna # if there are no extra nucleotides, the coding strand is dna

    for x in range(0,len(coding_strand),3):
        AA_chain +=  aa_table[dna[x:x+3]]
  
    return AA_chain

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.

        There are no doctests for this function because of its dependance on
        the longest_ORF_noncoding function, which depends on the randomized 
        shuffle_string function
    """
    
    thresh = longest_ORF_noncoding(dna,1500) 
    
    all_ORFs = find_all_ORFs(dna)
     
    amino_acids = []
    for x in range(len(all_ORFs)):
        if len(all_ORFs[x])> thresh:
            amino_acids.append(coding_strand_to_AA(all_ORFs[x]))  

    return amino_acids   

dna = load_seq("./data/X73525.fa")
amino_acids = gene_finder(dna)
print amino_acids

if __name__ == "__main__":
    import doctest
    doctest.testmod()