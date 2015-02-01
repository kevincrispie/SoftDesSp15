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
    """ flattens a list. I might use this function later on in 
    the program for the get_all_ORFs function
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

    EDIT: This new versione considers this possibility
    
    """ 
    TAG_index = dna.find('TAG')
    TAA_index = dna.find('TAA')
    TGA_index = dna.find('TGA')

    TAG_indices = [i for i in range(len(dna)) if dna.startswith('TAG',i)]
    TAA_indices = [i for i in range(len(dna)) if dna.startswith('TAA',i)]
    TGA_indices = [i for i in range(len(dna)) if dna.startswith('TGA',i)]

    TAG_isa3 = [1]*len(TAG_indices)
    TAA_isa3 = [1]*len(TAA_indices)
    TGA_isa3 = [1]*len(TGA_indices)

    for x in range(0,len(TAG_indices)):
        TAG_isa3[x] = TAG_indices[x]%3

    for x in range(0,len(TAA_indices)):
        TAA_isa3[x] = TAA_indices[x]%3

    for x in range(0,len(TGA_indices)):
        TGA_isa3[x] = TGA_indices[x]%3
           

    if 'TAG' not in dna and 'TAA' not in dna and 'TGA' not in dna:
        return dna

    
    elif 0 in TAG_isa3:
        TAG_first = TAG_indices[TAG_isa3.index(0)]
        frame=dna[0:TAG_first]
        return frame

    elif 0 in TAA_isa3:
        TAA_first = TAA_indices[TAA_isa3.index(0)]
        frame=dna[0:TAA_first]
        return frame

    if 0 in TGA_isa3:
        TGA_first = TGA_indices[TGA_isa3.index(0)]
        frame=dna[0:TGA_first]
        return frame

    else:
        return dna


"""
    if 'TAG' not in dna and 'TAA' not in dna and 'TGA' not in dna:
        return dna
    
    elif TAG_index != -1 and TAG_index%3 == 0:
        dna=dna[0:TAG_index]
        return dna

    elif TAA_index != -1 and TAA_index%3 == 0:
        dna=dna[0:TAA_index]
        return dna

    elif TGA_index != -1 and TGA_index%3 == 0:
        dna=dna[0:TGA_index]
        return dna

    else:
        return dna
"""

   

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
    # function runs until no dna is left (hence while>0)
    #below is an attmept to modify it to exclude ORFs with no stop codon,
    # but this version wants them 
    """
    TAG_indices = [i for i in range(len(dna)) if dna.startswith('TAG',i)]
    TAA_indices = [i for i in range(len(dna)) if dna.startswith('TAA',i)]
    TGA_indices = [i for i in range(len(dna)) if dna.startswith('TGA',i)]
    stop_indices = [TAG_indices, TAA_indices, TGA_indices]
    stop_indices = sum(stop_indices,[])
    stop_indices.sort()
    """
    frames=[]

    #dna = dna[:stop_indices[-1]+3]
    while len(dna)>0:
        frames.append(rest_of_ORF(dna))
        dna = dna[len(frames[0])+3:]
        

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
    #note: I'm not happy with the way I put the different lists together.
    #I'd like to find a more effecient way

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

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    #for DNA 
    """
    TAG_indices = [i for i in range(len(dna)) if dna.startswith('TAG',i)]
    TAA_indices = [i for i in range(len(dna)) if dna.startswith('TAA',i)]
    TGA_indices = [i for i in range(len(dna)) if dna.startswith('TGA',i)]
    stop_indices = [TAG_indices, TAA_indices, TGA_indices]
    stop_indices = sum(stop_indices,[])
    stop_indices.sort()

    dna_comp = get_reverse_complement(dna)
    TAG_indices_comp = [i for i in range(len(dna)) if dna_comp.startswith('TAG',i)]
    TAA_indices_comp = [i for i in range(len(dna)) if dna_comp.startswith('TAA',i)]
    TGA_indices_comp = [i for i in range(len(dna)) if dna_comp.startswith('TGA',i)]
    stop_indices_comp = [TAG_indices_comp, TAA_indices_comp, TGA_indices_comp]
    stop_indices_comp = sum(stop_indices_comp,[])
    stop_indices_comp.sort()


    mod_dna = dna[:stop_indices[-1]]
    mod_comp = dna_comp[:stop_indices_comp[-1]]
    """
    dna_comp = get_reverse_complement(dna)
    strand1 = dna
    strand2 = dna_comp
    #print 'for dna'
    frames_strand1 = find_all_ORFs(strand1)
    #print frames_strand1
    #print 'for complement'
    frames_strand2 = find_all_ORFs(strand2)
    #print frames_strand2
    #print '\n\n'
    #print find_all_ORFs('ATGTAGCATCAAA')

    both_strand_frames = [frames_strand1, frames_strand2]
    both_strand_frames = sum(both_strand_frames,[])
    return both_strand_frames
    


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    # TODO: implement this
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
    get_complement('A')
    get_complement('T')
    import doctest
    doctest.testmod()