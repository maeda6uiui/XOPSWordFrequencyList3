import argparse
import json
import yaml
from logging import getLogger,config
from pathlib import Path
from tqdm import tqdm

def main(args):
    input_root_dirname:str=args.input_root_dirname
    output_filepath:str=args.output_filepath

    #Set up logger
    with open("./logging_config.yaml","r",encoding="utf-8") as r:
        logging_config=yaml.safe_load(r)
    
    config.dictConfig(logging_config)

    logger=getLogger(__name__)
    logger.debug(args)

    #Get list of MIF files and MSG files
    input_root_dir=Path(input_root_dirname)
    mif_files=list(input_root_dir.glob("MIF/*.mif"))
    msg_files=list(input_root_dir.glob("MSG/*.msg"))

    logger.info(f"{len(mif_files)} MIF files exist in the input directory")
    logger.info(f"{len(msg_files)} MSG files exist in the input directory")

    #Get texts from MIF files
    logger.info("Start getting texts from MIF files...")
    mif_texts:list[str]=[]
    for mif_file in tqdm(mif_files):
        with mif_file.open("r",encoding="shift-jis",errors="ignore") as r:
            lines=r.read().splitlines()
            
        briefing_text="".join(lines[9:])
        mif_texts.append(briefing_text)

    #Get texts from MSG files
    logger.info("Start getting texts from MSG files...")
    msg_texts:list[str]=[]
    for msg_file in tqdm(msg_files):
        with msg_file.open("r",encoding="shift-jis",errors="ignore") as r:
            text=r.read()
            msg_texts.append(text)

    #Output texts to JSON file
    data={
        "mif": mif_texts,
        "msg": msg_texts,
    }
    with open(output_filepath,"w",encoding="utf-8") as w:
        json.dump(data,w,ensure_ascii=False)

    logger.info("Finished getting texts")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input-root-dirname",type=str)
    parser.add_argument("-o","--output-filepath",type=str)
    args=parser.parse_args()

    main(args)
