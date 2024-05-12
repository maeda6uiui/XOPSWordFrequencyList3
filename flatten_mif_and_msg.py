import argparse
import shutil
import yaml
from logging import getLogger,config
from pathlib import Path
from tqdm import tqdm

def main(args):
    input_root_dirname:str=args.input_root_dirname
    output_root_dirname:str=args.output_root_dirname

    #Set up logger
    with open("./logging_config.yaml","r",encoding="utf-8") as r:
        logging_config=yaml.safe_load(r)
    
    config.dictConfig(logging_config)

    logger=getLogger(__name__)
    logger.debug(args)

    #Get list of MIF files and MSG files
    input_root_dir=Path(input_root_dirname)
    mif_files=list(input_root_dir.glob("**/*.mif"))
    msg_files=list(input_root_dir.glob("**/*.msg"))

    logger.info(f"{len(mif_files)} MIF files exist in the input directory")
    logger.info(f"{len(msg_files)} MSG files exist in the input directory")

    #Create output directories
    output_root_dir=Path(output_root_dirname)
    output_root_dir.mkdir(exist_ok=True,parents=True)

    mif_output_dir=output_root_dir.joinpath("MIF")
    mif_output_dir.mkdir(exist_ok=True)

    msg_output_dir=output_root_dir.joinpath("MSG")
    msg_output_dir.mkdir(exist_ok=True)

    #Collect MIF files
    logger.info("Start collecting MIF files...")
    for idx,mif_file in enumerate(tqdm(mif_files)):
        output_file=mif_output_dir.joinpath(f"{idx}.mif")
        shutil.copy(mif_file,output_file)

    #Collect MSG files
    logger.info("Start collecting MSG files...")
    for idx,msg_file in enumerate(tqdm(msg_files)):
        output_file=msg_output_dir.joinpath(f"{idx}.msg")
        shutil.copy(msg_file,output_file)

    logger.info("Finished collecting files")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input-root-dirname",type=str)
    parser.add_argument("-o","--output-root-dirname",type=str)
    args=parser.parse_args()

    main(args)
