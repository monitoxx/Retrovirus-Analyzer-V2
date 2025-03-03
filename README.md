# Retrovirus-Analyzer-V2
Program made for analyzing retrovirus sequences thought-to-be HIV with sequences from an HIV database and finding similarity between them on a specified gene. Examples made with 'gag' Gene. This is the repository created for the final project of the subject Programming fundamentals for biological sciences. National University of Colombia (UNAL).

#### For using this program it's neccesary to refer to my package, found in https://github.com/monitoxx/basicbiofunctions

## The steps for gathering the database correctly from genbank are easy and as follows:
 1) Head to NCBI virus through the link https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/ 
 2) Type on the search bar the complete name of the virus you would like to analyze, in this case: "<ins>_human immunodeficiency virus_</ins>" or something similar, and select the taxid you want. 
![image](https://github.com/user-attachments/assets/9c4ded71-b17f-4f29-913e-0eb4ce14e293)
 3)  Now, head over to the "Refine results" option, and select the criteria you prefer for the analysis. In this case, nucleotide completeness (complete) and Has proteins option (type the gene you are looking for, in this case, gag). ![image](https://github.com/user-attachments/assets/22bb4eaa-af39-4e02-a06e-5ab589d53172)
 4)  Click the "Download option", choose: nucleotide> download all records> build custom. Select the options you'd like. Example: ![image](https://github.com/user-attachments/assets/e8d84e75-12ef-4fe7-8e78-0fee640b7735)

## IMPORTANT NOTE: It´s very important to notice that the programm as it is will only work from the terminal/console because of the sys.argv codes.
### The parameters must be inserted in the following order:
1. sample_sequence, The problem sequence downloaded in cds format from Genbank
2. database_file_name, The database downloaded from Genbank
3. gene_name, The exact gene name as in the sequence; for example: [gene=gag]

### How it should look:
    python .\retrovirus_analyzer_v2.py .\positive_control.txt .\vih_gag_database.fasta [gene=gag]

### From line 57-59 there is a commented section that can be used for local running on the text editor or IDLE, where the  information can be entered manually.

## Explanation for getting pylatex and the compiler running:
1) First of all, install pylatex package from your dedicated Python Integrated Development Environment (IDE)
2) Install the LaTeX compiler independently from the source you prefer, an option would be: https://miktex.org/download ![image](https://github.com/user-attachments/assets/61b30e7e-f73d-4aa9-9aed-88eb4292ad13)
3) Install strawberry in order for your compiler to run: https://strawberryperl.com ![image](https://github.com/user-attachments/assets/def9e094-e50f-4cd6-b31a-31e35212205c)
4) It's going to throw some errors at first, but you just have to allow the compiler to download the complimentary packages, it does it automatically when you authorize. 

## Results: 
 1) The output from the code in the terminal is:
![image](https://github.com/user-attachments/assets/ae34624d-611c-4ff8-b3ba-b658749b8caa)
 2) The code generates each of the graphics in jpg format
 3) The analysis report is created with pylatex and pdflatex tools and generated in pdf format

  


