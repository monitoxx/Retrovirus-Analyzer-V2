
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.errors import EmptyDataError
from pylatex import Document, Section, Subsection, Figure, Command, Enumerate
from pylatex.utils import NoEscape
import os
import timeit
import pandas as pd
from scipy.stats import ttest_1samp
import sys

from basicbiofunctions import df_creator, database_sample


"""
Please, read the README.md and LICENSE files beforehand in my GitHub repository:
https://github.com/monitoxx/Retrovirus-Analyzer

The following code was made by me (https://github.com/monitoxx) , with some help from Gemini Assistant and ChatGpt for 
finding errors and helping develop the LaTeX part of my code.
The comments provide a really self-explanatory experience from now on.
Reach me at my email for any doubts: ljimenezbe@unal.edu.co
"""

'''
IMPORTANT NOTE: It´s very important to notice that the programm as it is will only work from the terminal/console because of the sys.argv codes.
The parameters must be inserted in the following order:

        1. file_name_1, sequences downloaded in cds format from Genbank
        2. file_name_2, sequences downloaded in cds format from Genbank
        3. file_name_3, sequences downloaded in cds format from Genbank
        4. file_name_4, sequences downloaded in cds format from Genbank
        5. file_name_5, sequences downloaded in cds format from Genbank
        6. file_name_6, sequences downloaded in cds format from Genbank
        7. number_of_sequences, in this case, the previous 6
        8. gene_name, the exact gene name as in the sequence; [gene=gag]

How it should look:
'''
#  python .\retrovirus_analysis_plotter.py  .\sequence.txt .\sequence (1).txt .\sequence (2).txt .\sequence (3).txt .\sequence (4).txt .\sequence (5).txt 6 [gene=gag]
'''
From line 131-140 there is a commented section that can be used for local running on the text editor or IDLE, where the 
information can be entered manually.
'''

####Input from command line on the terminal####
# -----You can modify the following depending on how many sequences you want to analyze

sample_sequence = sys.argv[1]           #The problem sequence
database_file_name = sys.argv[2]           #The database
gene_name = sys.argv[3]             #The gene name


######Local variables########
'''
sample_sequence = 'positive_control.txt'
database_file_name = 'vih_gag_database.fasta'
gene_name = '[gene=gag]'
'''
gene_name_database_sample = gene_name.split('=')[1][:-1]
#print(gene_name_database_sample)

######Analysis by percentage of Guanine-Cytosine between the sample sequence and the first 9 sequences from the database######

sequences_list = database_sample(database_file_name, gene_name_database_sample)
sequences_list.append(sample_sequence)
#print(sequences_list)
number_of_sequences = len(sequences_list)-1


df_sequences, length, df_gc_content, df_gc_content_lists, df_gc_content_lists_exploded, heatmap_data = df_creator(sequences_list, gene_name)

# Verify data
#print(df_sequences,)
#print(df_gc_content,)
#print(df_gc_content_lists,)
#print(df_gc_content_lists_exploded,)
#print(length,)
#print(heatmap_data,)
genbank_code_list_ = ', '.join(df_sequences['GenBank Code'])
#print(genbank_code_list_)
target_sequence = genbank_code_list_[-10:]
#print(target_sequence)
genbank_code_list__ = genbank_code_list_.strip(target_sequence)
#print(genbank_code_list__)
genbank_code_list = genbank_code_list__.rstrip(', ')
#print(genbank_code_list)
print(target_sequence)



######BLAST ANALYSIS SECTION######

database_name = os.path.splitext(database_file_name)[0]
print(database_name)
command_database = f'makeblastdb -in {database_file_name} -dbtype nucl -out {database_name}'
os.system(command_database)

query = sample_sequence
output_file = "blastn_results.tsv"
output_format = "6 qseqid sseqid pident mismatch qstart qend length sstart send slen stitle qseq"

print(f'### Executing BLASTN with query {query} and subject {database_name}')
start = timeit.timeit()
print(f'Start time: {start}')

command_blast = f'blastn -query {query} -db {database_name} -outfmt "{output_format}" -out {output_file}'
print(command_blast)

os.system(command_blast)

print('### BLASTN finished ###')
end = timeit.timeit()
print(f'End time {end}')
print(f'Time taken: {end - start}')

# Loads results from blastn to a Dataframe
try:
    blast_results = pd.read_csv(output_file, sep="\t", comment="#", header=None)
    blast_results.columns = ["qseqid", "sseqid", "pident", "mismatch", "qstart",
                             "qend", "length", "sstart", "send", "slen", "stitle", "qseq"]
    # Calculate the statistics
    mean_pident = blast_results["pident"].mean()
    maximum_value = max(blast_results['pident'])
    minimum_value = min(blast_results['pident'])
    # print(maximum_value)
    # print(minimum_value)
    median_pident = blast_results["pident"].median()
    std_pident = blast_results["pident"].std()

    t_stat, p_value = ttest_1samp(blast_results["pident"], popmean=90)  # Comparing with 90%

except EmptyDataError:
    mean_pident = 0
    maximum_value = 0
    minimum_value = 0
    median_pident = 0
    std_pident = 0
    t_stat = 0
    p_value = 0

    pass




######GRAPHICS#############
# Graphics of density
plt.figure(1, figsize=(11,6))

plt.subplot(1,2,1)
sns.kdeplot(data=df_gc_content_lists_exploded, x='% GC Content', hue='GenBank Code', fill=True)
plt.title('Density of % GC Content by GenBank Code')
plt.xlabel('% GC Content')
plt.ylabel('Density')
plt.grid(True)

plt.subplot(1,2,2)
sns.kdeplot(data=df_gc_content_lists_exploded, x='% GC Content Random', hue='GenBank Code', fill=True)
plt.title('Density of % GC Content Random by GenBank Code')
plt.xlabel('% GC Content Random')
plt.ylabel('Density')
plt.grid(True)
plt.tight_layout()
plt.savefig('density_gc.jpg', dpi=600)
plt.close()

# Scatterplot of % GC Content by position and GenBank Code with regression lines
sns.lmplot(x='Position', y='% GC Content', data=df_gc_content_lists_exploded, hue='GenBank Code',
           scatter_kws={'alpha':0.5})
#plt.title('Dispersion and regression lines for % GC Content by position')
plt.xlabel('Position')
plt.ylabel('% GC Content')
plt.grid()
plt.savefig('scatterplot_gc.jpg', dpi=600)
plt.close()

#Histogram + Kde plot for frequency of percentage of identity
if mean_pident != 0:
    plt.figure(figsize=(8,5))
    sns.histplot(blast_results["pident"], bins=20, kde=True, color="blue", alpha=0.4)
    plt.xlabel("Percentage Identity (%)")
    plt.ylabel("Frequency / Density")
    plt.title("Histogram of BLASTN Identity Percentages")
    plt.grid(True)
    plt.savefig('hist_kde_pident.jpg', dpi=600)
    plt.close()
else:
    plt.savefig('hist_kde_pident.jpg', dpi=600)

####################################### Creates the LaTeX Document#########################################
doc = Document()

# Document title
doc.preamble.append(NoEscape(r'\usepackage[headheight=20pt, top=2cm]{geometry}'))
doc.preamble.append(Command('title', f'Analysis report for the "{gene_name_database_sample}" gene in {number_of_sequences} supposedly alike sequences from a database'))
doc.preamble.append(Command('author', 'Luis Jimenez'))
doc.preamble.append(Command('date', NoEscape(r'\today')))
doc.append(NoEscape(r'\maketitle'))

# Section
with doc.create(Section('Introduction')):
    doc.append(f'The analyzed sequence extracted from GeneBank is {target_sequence}, '
               f'and the sequences used for the comparison by %GC content were extracted from a database '
               f'only with genomes that have the target gene, which are as follows: {genbank_code_list}. Additionally, '
               f'a comprehensive BLASTN analysis against the database was executed to calculate the percentage identity, '
               f"suggesting potential validation of the target sequence's similarity to those from the database.")

# Graphics
with doc.create(Section('Graphic comparison via GC content')):

    with doc.create(Subsection('Density of % GC Content and % GC Content for the randomized sequences')):
        with doc.create(Figure(position='!htbp')) as graphic1:
            graphic1.add_image('density_gc.jpg', width=NoEscape(r'1\textwidth'))
            graphic1.add_caption('Density of % GC content in the sequences analyzed by fragments at a time.')

    with doc.create(Subsection('Scatterplot of % GC Content by position and GenBank Code with regression lines')):
        with doc.create(Figure(position='!htbp')) as graphic3:
            graphic3.add_image('scatterplot_gc.jpg', width=NoEscape(r'0.8\textwidth'))
            graphic3.add_caption('Dispersion and regression lines for % GC Content by position')

with doc.create(Section('BLASTN Analysis Results')):
    if mean_pident != 0:
        doc.append(f"The BLASTN analysis was performed to identify homologous sequences to the target sequence "
                   f"within the NCBI nucleotide database. The results were saved in the file {output_file}. "
                   f"The columns in the output correspond to: Query sequence ID, Subject sequence ID, Percentage "
                   f"of identical matches, Number of mismatches, Start of alignment in query, End of alignment in query, "
                   f"Alignment length, Start of alignment in subject, End of alignment in subject, Subject sequence "
                   f"length, Subject title, Aligned part of query sequence.\n")

        doc.append(f"\nThe average identity percentage across all alignments is {mean_pident:.2f}%, "
               f"with a median of {median_pident:.2f}% and a standard deviation of {std_pident:.2f}%. The maximum identity"
               f" percentage found in the BLASTN analysis was {maximum_value:.2f}% and the minimum {minimum_value:.2f}%. ")

        # Statistical analysis (t-test)
        if p_value < 0.05:  # Bilateral test
            if t_stat > 0:
                doc.append("A statistical test (one-sample t-test) indicates that the mean identity percentage is higher than 90% "
                       f"(t = {t_stat:.2f}, p = {p_value:.6f}). This supports a strong similarity between the analyzed sequences and the database.")
            else:
                doc.append("A statistical test (one-sample t-test) indicates that the mean identity percentage is lower than 90% "
                       f"(t = {t_stat:.2f}, p = {p_value:.6f}). This suggests that the sequences may have important differences compared to the database.")
        else:
            doc.append("The statistical analysis does not provide strong evidence that the mean identity percentage differs from 90% "
                   f"(t = {t_stat:.2f}, p = {p_value:.6f}). This means the sequence similarity remains inconclusive.")

        with doc.create(Subsection('Histogram with density line of BLASTN Identity Percentages')):
            doc.append(f"The following graphic is good for visualizing the frequency at which every percentage of identity"
                   f" is distributed so that the reader can make a more assertive decision based on all previous factors.\n\n ")

            if maximum_value == 100:
                doc.append(f"The maximum value of identity percentage hits 100% at least once, hence, a strong conclusion "
                       f"is that the sequence {target_sequence} can be, in fact, a strain of the family of sequences in the "
                       f"database used because it is the same as at least one of them. \n\nIn this case, the statistical analysis "
                       f"can be either useless or useful because of this factor, and also as seen in the previous graphics, the similarities are"
                       f" higher than the discrepancies. ")

            with doc.create(Figure(position='!htbp')) as graphic4:
                graphic4.add_image('hist_kde_pident.jpg', width=NoEscape(r'1\textwidth'))
                graphic4.add_caption('Frequency of identity percentages in BLASTN analysis.')
    else:
        doc.append(f'The BLASTN analysis was performed to identify homologous sequences to the target sequence '
                   f'within the NCBI nucleotide database. The results revealed no significant matches, indicating '
                   f'a complete absence of detectable sequence similarity. This suggests that the target sequence '
                   f'does not share significant homology with any sequences currently deposited in the database.')


# Compile the document
doc.generate_pdf('results_report' ,compiler='pdflatex', clean_tex=False)
print('PDF generated as results_report.pdf')