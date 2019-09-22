import numpy as np                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
import pandas
import os
import itertools

def main():
    filename = "Pong"
    
    spice_filetype = "cir"
    spice_folder = "SPICE inputs"

    output_folder = "Parser Out"
    output_filetype = "csv"

    input_file = os.path.join(spice_folder,filename+"."+spice_filetype)
    output_file = os.path.join(output_folder,filename+"."+output_filetype)

    ReadSpiceNetlist(input_file)


def ReadSpiceNetlist(filepath):
    #get each line of the spice netlist as an entry in an array (split by \n)
    with open(filepath, "rb") as data:
        #LT Spice why would you use utf-16-le? Can I use emoji in netnames??
        content = data.read().decode("utf-16-le")
    #remove leading/trailing whitespace and the \n character from each line
    content = content.split("\n")
    
    #tokenize each line splitting by whitespace 
    # (Not a big deal since we don't use these anywhere, 
    # but ideally we want to not split filepaths that have spaces in them!!!)
    content = [line.split() for line in content]

    #make into rectangular array
    contentRectPerp = list(itertools.zip_longest(*content))
    contentRect = list(itertools.zip_longest(*contentRectPerp))

    #all the lines in between the first comment and second comment
    topLevelRect = GetTopLevelLines(contentRect)
    
    #all the lines that start with .subckt
    subcktRect = list(filter(lambda line: line[0]=='.subckt', contentRect))

    x=2

    return

def GetTopLevelLines(contentRect):
    #get the top level circuit components
    '''
    We can identify this area because it will be between two comments. 
    Comments start by "* "
    The first comment will be "* {filepath}"
    The second comment will be "* block symbol definitions"    
    '''
    include = 0
    topLevelRect = []
    for line in contentRect:
        if include == 2:
            break
        if include:
            topLevelRect.append(line)
        if line[0]=='*':
            include += 1
    return topLevelRect
    

def CreateAdjacencyMatrix(topLevelPins, subcktPinDefs):
    #for each component in the topLevel netlist, add a bunch of columns to pandas df
    return

if __name__ == '__main__':
    main()
