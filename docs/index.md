
# AnnoKit

Reference genome annotation file processing toolset

## main functions

- `searchs`: given a genome range, find genes within the range and related information about the gene.

- `maps`: direct related query between gene name(symbol) and gene ID(Ensembl).

- `inquires`: given one or more gene names or IDs, query the detailed information of the corresponding genes, transcripts, exons and other related gene structures.

## gene structure

### eukaryote

<div align="center">

<img src="./imgs/Gene_structure_eukaryote.png">

</div>

### prokaryote

<div align="center">

<img src="./imgs/Gene_structure_prokaryote.png">

</div>

## install

### pip

```shell
pip install AnnoKit
```

## GTF

gtf file analysis

- [GTF](https://github.com/iOLIGO/AnnoKit/blob/main/docs/GTF.md)
