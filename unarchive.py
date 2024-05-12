import argparse
import shutil
import yaml
from logging import getLogger,config
from pathlib import Path
from tqdm import tqdm

def main(args):
    input_dirname:str=args.input_dirname
    output_root_dirname:str=args.output_root_dirname

    #Set up logger
    with open("./logging_config.yaml","r",encoding="utf-8") as r:
        logging_config=yaml.safe_load(r)
    
    config.dictConfig(logging_config)

    logger=getLogger(__name__)
    logger.debug(args)

    #Get list of ZIP files in the input directory
    input_dir=Path(input_dirname)
    input_files=list(input_dir.glob("*.zip"))

    logger.info(f"{len(input_files)} files exist in the input directory")

    #Create output directory
    output_root_dir=Path(output_root_dirname)
    output_root_dir.mkdir(exist_ok=True,parents=True)

    #Unarchive files
    logger.info("Start unarchiving files...")
    for idx,input_file in enumerate(tqdm(input_files)):
        output_dir=output_root_dir.joinpath(f"{idx}")
        output_dir.mkdir(exist_ok=True)

        shutil.unpack_archive(input_file,output_dir)

    logger.info("Finished unarchiving files")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input-dirname",type=str)
    parser.add_argument("-o","--output-root-dirname",type=str)
    args=parser.parse_args()

    main(args)
