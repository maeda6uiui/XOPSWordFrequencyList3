import argparse
import shutil
import yaml
from logging import getLogger,config
from pathlib import Path
from tqdm import tqdm

def main(args):
    input_root_dirname:str=args.input_root_dirname
    output_dirname:str=args.output_dirname

    #Set up logger
    with open("./logging_config.yaml","r",encoding="utf-8") as r:
        logging_config=yaml.safe_load(r)
    
    config.dictConfig(logging_config)

    logger=getLogger(__name__)
    logger.debug(args)

    #Get list of ZIP files in the input directory
    input_root_dir=Path(input_root_dirname)
    input_files=list(input_root_dir.glob("**/*.zip"))

    logger.info(f"{len(input_files)} files exist in the input directory")

    #Create output directory
    output_dir=Path(output_dirname)
    output_dir.mkdir(exist_ok=True,parents=True)

    #Flatten the files
    logger.info("Start flattening archive files...")
    for idx,input_file in enumerate(tqdm(input_files)):
        output_file=output_dir.joinpath(f"{idx}.zip")
        shutil.copy(input_file,output_file)

    logger.info("Finished flattening archive files")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input-root-dirname",type=str)
    parser.add_argument("-o","--output-dirname",type=str)
    args=parser.parse_args()

    main(args)
