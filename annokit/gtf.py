import types
import warnings
from dataclasses import field, dataclass
from typing import Any, List
from intervaltree import IntervalTree, Interval


@dataclass
class BASE:
    chr:str
    start:int
    end:int
    strand:str
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError(f"{name}' cannot be modified.")
        super().__setattr__(name, value)


@dataclass
class EXON(BASE):
    id:str


class TRANSCRIPT:
    """
    """
    def __init__(self, trans_id:str, trans_name:str, chr:str, start:int, end:int, strand:str):
        self.id = trans_id
        self.name = trans_name
        self.chr = chr
        self.start = start
        self.end = end
        self.strand = strand
        self.CDS = [] # List[BASE]
        self.start_codon = [] # List[BASE]
        self.stop_codon = [] # List[BASE]
        self.UTR5 = [] # List[BASE]
        self.UTR3 = [] # List[BASE]
        self.exons = {}
        self.other = [] # List[BASE]


    def add_exon(self, exon:EXON):
        if exon.id == "NONE":
            exon.id = f"exon_{len(self.exons) + 1}"
        self.exons[exon.id] = exon
    

    def add_start_codon(self, start_codon:BASE):
        self.start_codon.append(start_codon)
    
    def add_stop_codon(self, stop_codon:BASE):
        self.stop_codon.append(stop_codon)
    
    def add_UTR5(self, UTR5):
        self.UTR5.append(UTR5)
    
    def add_UTR3(self, UTR3):
        self.UTR3.append(UTR3)
    
    def add_CDS(self, CDS:BASE):
        self.CDS.append(CDS)
    
    def add_other(self, other:BASE):
        self.other.append(other)



class GENE:
    """
    """

    def __init__(self, gene_id:str, gene_name:str, chr:str, start:int, end:int, strand:str):
        self.id = gene_id
        self.name = gene_name
        self.chr = chr
        self.start = start
        self.end = end
        self.strand = strand
        self.trans = {}
        self.trans_map = {}
    

    def add_trans(self, trans:TRANSCRIPT):
        self.trans[trans.id] = trans
        self.trans_map[trans.name] = trans.id

def Bases_dict(bases:str) -> dict:
    bases_dict = {}
    for base in bases.split(";"):
        base_list = base.split('"')
        if len(base_list) > 1:
            name = base_list[0].strip()
            content = base_list[1].strip()
            bases_dict[name] = content
    return bases_dict

def Gtf_block(gtf_file:str) -> types.GeneratorType:

    with open(gtf_file, "r") as f:

        blocks = []
        for line in f:
            if line.startswith("#"):
                continue
            
            line_list = line.strip().split("\t")
            if len(line_list) < 8:
                continue

            anno_type = line_list[2]
            if anno_type == "gene":
                if len(blocks) == 0:
                    pass
                else:
                    yield blocks
                    blocks = []
            blocks.append(line.strip())
        
        if blocks:
            yield blocks


#anno_map = anno_name1,gtf_str2;anno_name2,gtf_str2;...
class GTF:
    """
    """
    def __init__(self, name=None, version=None, URL=None, anno_map=None):
        self.name = name
        self.version = version
        self.URL = URL
        self.genes = {}
        self.genes_map = {}
        self.genes_interval = {}
        self.err = []
        self.anno_map = {"gene":"gene", "trans":"transcript", "exon":"exon",
                         "CDS":"CDS", "start_codon":"start_codon",
                         "stop_codon":"stop_codon", "UTR5":"five_prime_utr",
                         "UTR3":"three_prime_utr", "other":"other"}
        if anno_map:
            for bases in anno_map.split(";"):
                name = bases[0]
                gtf_str = bases[1]
                if name in self.anno_map:
                    self.anno_map[name] = gtf_str
                else:
                    warnings.warn(f"annotation map err: {name}; maby use key words 'other'", Warning)


    

    def add_gene(self, gene:GENE):
        self.genes[gene.id] = gene
        self.genes_map[gene.name] = gene.id
    
    def add_err(self, err:str):
        self.err.append(err)
    
    def read(self, gtf, name=None, version=None, URL=None):
        self.name = name
        self.version = version
        self.URL = URL

        blocks = Gtf_block(gtf)

        for block in blocks:
            for line in block:
                chrn, tmp1, anno_type, start, end, tmp2, strand, tmp3, bases = line.split("\t")
                start = int(start)
                end = int(end)
                bases_dict = Bases_dict(bases)

                if anno_type == self.anno_map["gene"]:
                    # gene name
                    if "gene_name" in bases_dict:
                        gene_name = bases_dict["gene_name"]
                    else:
                        gene_name = bases_dict["gene_id"]
                    
                    gene = GENE(bases_dict["gene_id"], gene_name, chrn, start, end, strand)
                
                elif anno_type == self.anno_map["transcript"]:
                    # transcript name
                    if "transcript_name" in bases_dict:
                        trans_name = bases_dict["transcript_name"]
                    else:
                        trans_name = bases_dict["transcript_id"]
                    trans = TRANSCRIPT(bases_dict["transcript_id"], trans_name, 
                                       chrn, start, end, strand)
                    gene.add_trans(trans)
                
                elif anno_type == self.anno_map["exon"]:
                    # exon_id
                    if bases_dict["exon_id"]:
                        exon = EXON(chrn, start, end, strand, bases_dict["exon_id"])
                    else:
                        exon = EXON(chrn, start, end, strand, "NONE")
                    
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_exon(exon)
                
                elif anno_type == self.anno_map["CDS"]:
                    cds = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_CDS(cds)
                
                elif anno_type == self.anno_map["start_codon"]:
                    start_codon = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_start_codon(start_codon)
                
                elif anno_type == self.anno_map["stop_codon"]:
                    stop_codon = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_stop_codon(stop_codon)
                
                elif anno_type == self.anno_map["five_prime_utr"]:
                    utr5 = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_UTR5(utr5)
                
                elif anno_type == self.anno_map["three_prime_utr"]:
                    utr3 = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_UTR3(utr3)

                elif anno_type == self.anno_map["other"]:
                    other = BASE(chrn, start, end, strand)
                    trans_id = bases_dict["transcript_id"]
                    gene.trans[trans_id].add_other(other)
                
                else:
                    warnings.warn(f"annotation type err: {anno_type}", Warning)
                    self.add_err(line)
            
            self.add_gene(gene)
            # interval
            if gene.chr in self.genes_interval:
                chr_interval = self.genes_interval[gene.chr]
            else:
                chr_interval = IntervalTree()
            chr_interval.addi(gene.start, gene.end, data=gene.id)
            self.genes_interval[gene.chr] = chr_interval

        return
    
    # loc = chr:start:end
    def searchLoc(self, loc):
        chrn, start, end = loc.split(":")
        start = int(start)
        end = int(end)
        return self.genes_interval[chrn](start, end)


    # genes = {genename1};{genename2};...;{genenameN}
    def maps(self, genes, mapType="n2i"):
        dict_map = {}
        if mapType == "n2i":
            for name in genes.split(";"):
                if name in self.genes_map:
                    dict_map[name] = self.genes_map[name]
                else:
                    warnings.warn(f"not found genename {name} in gtf", Warning)
                    dict_map[name] = "None"

        elif mapType == "i2n":
            for id in genes.split(";"):
                if id in self.genes:
                    dict_map[id] = self.genes[id].name
                else:
                    warnings.warn(f"not found geneid {id} in gtf", Warning)
                    dict_map[id] = "None"
        else:
            raise ValueError("params err: please check mapType!")
        return dict_map



                


    

        

