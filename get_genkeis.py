import argparse
import json
import re
import yaml
from logging import getLogger,config
from pyknp import Juman
from tqdm import tqdm

def main(args):
    input_filepath:str=args.input_filepath
    output_filepath:str=args.output_filepath

    #Set up logger
    with open("./logging_config.yaml","r",encoding="utf-8") as r:
        logging_config=yaml.safe_load(r)
    
    config.dictConfig(logging_config)

    logger=getLogger(__name__)
    logger.debug(args)

    #Load texts from JSON
    with open(input_filepath,"r",encoding="utf-8") as r:
        data=json.load(r)

    texts:list[str]=data["mif"]+data["msg"]

    #Create Juman++ instance
    jumanpp=Juman()

    #Set up regexp to remove symbols
    re_symbols=re.compile('[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＜＞＄＃＠。、？！｀＋￥％ 　]')

    #Analyze morphemes and get genkeis
    logger.info("Start morpheme analysis and get genkeis...")
    
    genkeis:list[str]=[]
    for text in tqdm(texts):
        text=text.replace("\n","")
        text=re_symbols.sub("",text)

        analysis_result=jumanpp.analysis(text)
        for mrph in analysis_result.mrph_list():
            genkeis.append(mrph.genkei)

    #Output genkeis to a text file
    with open(output_filepath,"w",encoding="utf-8") as w:
        for genkei in genkeis:
            w.write(f"{genkei}\n")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input-filepath",type=str)
    parser.add_argument("-o","--output-filepath",type=str)
    args=parser.parse_args()

    main(args)
