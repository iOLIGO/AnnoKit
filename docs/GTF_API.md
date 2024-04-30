# GTF API

## python API

```python
from gtf_tools.gtf import GTF
```

## gtf_tools class

### BASE

CDS, start_codon, stop_codon, UTR5, UTR3, other and other annotation types use this class.

|Attributes|data type|info|
|:--------:|:-------:|:--:|
|chr|str|chromosome|
|start|int|location start|
|end|int|location end|
|strand|str|strand '+' or '-'|

more info: The attribute value of BASE is readable. That is, after reading from the gtf file for the first time, it cannot be modified.


### EXON

Record exon related information.

|Attributes|data type|info|
|:--------:|:-------:|:--:|
|chr|str|exon chromosome|
|start|int|exon location start|
|end|int|lexon ocation end|
|strand|str|exon strand '+' or '-'|
|id|str|exon id|

more info: The attribute value of BASE is readable. That is, after reading from the gtf file for the first time, it cannot be modified.


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
|trans_map|Dict\[TRANSCRIPT.name] = TRANSCRIPT.id


### GTF


