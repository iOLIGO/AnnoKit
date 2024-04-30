# GTF
## python API

```python
from annokit.gtf import GTF
from annokit.gtf import GTF
gtf = GTF()
gtf_file = "./test/test.gtf"
gtf.read(gtf_file, name="test", version="1.0", URL="none")
gtf.name
# 'test'
```

more info: The three parameters `name`, `version` and `URL` are all optional parameters. The main purpose is to record the relevant information of the gtf file.

## class

### BASE

CDS, start_codon, stop_codon, UTR5, UTR3, other and other annotation types use this class.

|Attributes|data type|info|
|:--------:|:-------:|:--:|
|chr|str|chromosome|
|start|int|location start|
|end|int|location end|
|strand|str|strand '+' or '-'|

more info: The attribute value of `BASE` is readable. That is, after reading from the gtf file for the first time, it cannot be modified.


### EXON

Record exon related information.

|Attributes|data type|info|
|:--------:|:-------:|:--:|
|chr|str|exon chromosome|
|start|int|exon location start|
|end|int|lexon ocation end|
|strand|str|exon strand '+' or '-'|
|id|str|exon id|

more info: The attribute value of `EXON` is readable. That is, after reading from the gtf file for the first time, it cannot be modified.


### TRANSCRIPT

Record transcript related information.

|Attributes|data type|info|
|:--------:|:-------:|:--:|
|id|str|transcript id|
|name|str|transcript name|
|chr|str|transcript location chromosome|
|start|int|transcript location start|
|end|int|transcript location end|
|strand|str|transcript strand '+' or '-'|
|CDS|List\[BASE\]|transcript CDSs|
|start_codon|List\[BASE\]|transcript start_codons|
|stop_codon|List\[BASE\]|transcript stop_codons|
|UTR5|List\[BASE\]|transcript UTR5s|
|UTR3|List\[BASE\]|transcript UTR3s|
|exons|Dict\[EXON.id\]=EXON|transcript exons|
|other|List\[BASE\]|transcript other annotation types|


### GENE

Record gene related information.

|Attributes|data type|info|
|:--------:|:-------:|:--:|
|id|str|gene id|
|name|str|gene name|
|chr|str|gene location chromosome|
|start|int|gene location start|
|end|int|gene location end|
|strand|str|gene strand '+' or '-'|
|trans|Dict\[TRANSCRIPT.id\]=TRANSCRIPT|gene transcripts|
|trans_map|Dict\[TRANSCRIPT.name] = TRANSCRIPT.id| map of id and name|


### GTF

Parse GTF files

|Attributes|data type|info|
|:--------:|:-------:|:--:|
|name|str|gtf name|
|version|str|gtf version|
|URL|str|download URL of gtf file|
|genes|Dict\[GENE.id\]=GENE|gtf genes|
|genes_map|Dict\[GENE.name\]=GENE.id|map of id and name|
|genes_interval|Dict\[chromosome]=IntervalTree|genes location projects to IntervalTree|


#### interval search

[intervaltree](https://github.com/chaimleib/intervaltree): a mutable, self-balancing interval tree for Python 2 and 3. Queries may be by point, by range overlap, or by range envelopment.

```python
from annokit.gtf import GTF
gtf = GTF()
gtf_file = "./test/test.gtf"
gtf.read(gtf_file, name="test", version="1.0", URL="none")
loc = "chr1:1000:5000"
genes = gtf.search(loc)
genes
# '[geneid1, geneid2, ..., geneidn]'
```

more info: The location parameter consists of the chromosome, starting position, and ending position, with a colon between them, like '`{chr}:{start}:{end}`'.


#### annotation type map

annotation type map, the corresponding description relationship between annotation attributes and annotation types description in annotation files.

##### raw map table

|Attributes|description|
|:--------:|:---------:|
|gene|gene|
|trans|transcript|
|exon|exon|
|CDS|CDS|
|start_codon|start_codon|
|stop_codon|stop_codon|
|UTR5|five_prime_utr|
|UTR3|three_prime_utr|
|other|other|

more info: `other` is an additional reserved attribute for reading special cases that do not exist in the table but exist in the gtf file.


##### map table description content replacement

```python
from annokit.gtf import GTF
gtf = GTF()
gtf_file = "./test/test.gtf"
anno_map = "UTR5,UTR5;other,other_anno"
gtf.read(gtf_file, name="test", anno_map=anno_map)
gtf.anno_map
# " {'gene': 'gene', 'trans': 'transcript', 'exon': 'exon', 'CDS': 'CDS', 'start_codon': 'start_codon', 'stop_codon': 'stop_codon', 'UTR5': 'UTR5', 'UTR3': 'three_prime_utr', 'other': 'other_anno'} "
```

more info: anno_map can modify the gtf description corresponding to multiple attributes at the same time, separated by semicolons, and the attributes and descriptions are separated by commas, like '`{attributes1},{description1};{attributes2},{description2};...;{attributesN},{descriptionN}`'





