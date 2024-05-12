import argparse
import yaml
from collections import Counter
from logging import getLogger,config

def main(args):
    input_filepath:str=args.input_filepath
    output_filepath:str=args.output_filepath

    #Set up logger
    with open("./logging_config.yaml","r",encoding="utf-8") as r:
        logging_config=yaml.safe_load(r)
    
    config.dictConfig(logging_config)

    logger=getLogger(__name__)
    logger.debug(args)

    #Load list of genkeis
    with open(input_filepath,"r",encoding="utf-8") as r:
        genkeis=r.read().splitlines()

    #Count frequencies of genkeis
    logger.info("Start counting frequencies of genkeis...")

    counter=Counter(genkeis)
    with open(output_filepath,"w",encoding="utf-8") as w:
        for genkei,freq in counter.most_common():
            w.write(f"{genkei}\t{freq}\n")

    logger.info("Finished counting frequencies of genkeis")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input-filepath",type=str)
    parser.add_argument("-o","--output-filepath",type=str)
    args=parser.parse_args()

    main(args)
