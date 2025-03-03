# Retrovirus-Analyzer-V2
Program made for analyzing retrovirus sequences thought-to-be HIV with sequences from an HIV database and finding similarity between them on a specified gene. Examples made with 'gag' Gene. This is the repository created for the final project of the subject Programming fundamentals for biological sciences. National University of Colombia (UNAL).

>[!WARNING]
>For using this program it's neccesary to refer to my package, found in [basicbiofunctions](https://github.com/monitoxx/basicbiofunctions)

## The steps for gathering the database correctly from genbank are easy and as follows:
 1) Head to NCBI virus through the link [NCBI Virus](https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/)
 2) Type on the search bar the complete name of the virus you would like to analyze, in this case: "<ins>_human immunodeficiency virus_</ins>" or something similar, and select the taxid you want. 
![image](https://github.com/user-attachments/assets/9c4ded71-b17f-4f29-913e-0eb4ce14e293)
 3)  Now, head over to the "Refine results" option, and select the criteria you prefer for the analysis. In this case, nucleotide completeness (complete) and Has proteins option (type the gene you are looking for, in this case, gag). ![image](https://github.com/user-attachments/assets/22bb4eaa-af39-4e02-a06e-5ab589d53172)
 4)  Click the "Download option", choose: nucleotide> download all records> build custom. Select the options you'd like. Example: ![image](https://github.com/user-attachments/assets/e8d84e75-12ef-4fe7-8e78-0fee640b7735)

>[!IMPORTANT]
>It's very important to notice that the programm as it is will only work from the terminal/console because of the sys.argv codes.
### The parameters must be inserted in the following order:
1. sample_sequence, The problem sequence downloaded in cds format from Genbank
2. database_file_name, The database downloaded from Genbank
3. gene_name, The exact gene name as in the sequence; for example: [gene=gag]

### How it should look:
    python .\retrovirus_analyzer_v2.py .\positive_control.txt .\vih_gag_database.fasta [gene=gag]

>[!TIP]
>From line 57-59 there is a commented section that can be used for local running on the text editor or IDLE, where the  information can be entered manually.

## Explanation for getting pylatex and the compiler running:
1) First of all, install pylatex package from your dedicated Python Integrated Development Environment (IDE)
2) Install the LaTeX compiler independently from the source you prefer, an option would be: [MiKTeX](https://miktex.org/download) <br/> ![image](https://github.com/user-attachments/assets/61b30e7e-f73d-4aa9-9aed-88eb4292ad13)
3) Install strawberry in order for your compiler to run: [StrawberryPearl](https://strawberryperl.com) <br/> ![image](https://github.com/user-attachments/assets/def9e094-e50f-4cd6-b31a-31e35212205c)
4) It's going to throw some errors at first, but you just have to allow the compiler to download the complimentary packages, it does it automatically when you authorize. 

> [!NOTE]
> The process for getting blast running is much easier, just refer to the official webpage and install it as you usually do with other programs: [BLAST+](https://blast.ncbi.nlm.nih.gov/doc/blast-help/downloadblastdata.html)

## Results: 
 1) An example of the output from the code in the terminal is:
![image](https://github.com/user-attachments/assets/c912316f-f25b-4307-8f40-ff70a52f82e0)
 2) Nine (9) output files are generated, these files are extracted from the database to elaborate the %GC content graphic comparison.
 3) One (1) output file is generated, it is called as the GenBank code of the sequence, it includes only the section from the sequence where the target gene is located, used for the BLASTN analysis.
 4) Eigth (8) outpufiles are generated, with the same name as the database file except for the suffixes, automatically created by the makblastdb command, corresponds to the database group of files.
 6) Three (3) images are generated, for each of the graphics in jpg format.
 7) One (1) tabular style file generated called blastn_results.tsv, it includes the results from the BLASTN analysis. The columns correspond for the following data, in the respective order:
    - Query sequence ID
    - Subject sequence ID
    - Percentage of identical matches
    - Number of mismatches
    - Start of alignment in query
    - End of alignment in query
    - Alignment length
    - Start of alignment in subject
    - End of alignment in subject
    - Subject sequence length
    - Subject title
    - Aligned part of query sequenc
 9) One (1) PDF file generated called results_report.pdf, the results report is created with pylatex and pdflatex tools.


  


