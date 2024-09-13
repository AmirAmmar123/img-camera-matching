from pnuidmapper import Mapper as mp 
from plotPnuIdHist import ImagePNUIDHistogram as ipnuidHis
from normlized_correlation_imgSet_pnu import PNUMatcher as pnm 
from optimized_averging_training_pnu import PNUMatcher as opnm
from preparing_data_for_gaussian_thresholding import DataProcessor as dp 
import json 
from joinData import AllData
from gaussian import TwoGaussian
import os 
from const import PNU 
import argparse


class CameraImageMatcher:
    def __init__(self, args):
        self.db_bath = args.db_bath
        self.data_dump = args.data_dump
        self.home_directory_path = args.home_directory_path
        self.base_directory = args.base_directory
        self.read_correlation_result = args.read_correlation_result
        self.save_to_gaussian_stage = args.save_to_gaussian_stage
        self.save_to_gaussian = args.save_to_gaussian
        self.create_x_pnu_id = args.create_x_pnu_id
        self.activate_creation = args.activate_creation
        self.activate_matcher = args.activate_matcher

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Camera Image Matcher")
        parser.add_argument("--db_bath", type=str, default='data-base', help="Path to the Data-Base")
        parser.add_argument("--data_dump", type=str, default="/data-base/results/", help="Path to Dump the output results")
        parser.add_argument("--home_directory_path", type=str, default="/home/ameer/img-camera-matching/", help="Home directory path")
        parser.add_argument("--base_directory", type=str, default="img-camera-matching/Data-Base", help="Base directory from the project directory to the data-base directory")
        parser.add_argument("--read_correlation_result", type=str, default="data-base/results/data.json", help="The correlation result between the data-base and the PNU ID will be saved here")
        parser.add_argument("--save_to_gaussian_stage", type=str, default="data-base/results/preparing_to_thresholding.json", help="Closest points between the data-base and PNU ID will be saved here")
        parser.add_argument("--save_to_gaussian", type=str, default='/home/ameer/img-camera-matching/data-base/results/gussians.json', help="Save the Gaussian results to this directory")
        parser.add_argument("--create_x_pnu_id", type=int, default=0, help="Number of PNU IDs to create")
        parser.add_argument("--activate_creation", type=bool, default=False, help="Activate the generation of PNU ID for each image data set")
        parser.add_argument("--activate_matcher", type=bool, default=False, help="Activate the correlation generation between image-set and PNU ID")
        return parser.parse_args()

    def ensure_directory_exists(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def dump_to_json(self, data, file_path, append=False):
        self.ensure_directory_exists(file_path)
        if append and os.path.exists(file_path):
            # Open the file and ensure it has valid JSON or initialize with empty list if needed
            with open(file_path, 'r+') as file:
                if content := file.read():
                    file.seek(0)
                    existing_data = json.load(file)
                else:
                    file.write('[]')
                    existing_data = []
                file.seek(0)
                json.dump(existing_data + data, file, indent=4)
        else:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)



    def run(self):
        if self.activate_creation:
            for id in range(self.create_x_pnu_id):
                mp_instance = mp(self.db_bath, id)
                mp_instance.transform_all_imges()
                mp_instance.create_ID().saveID()

        if self.activate_matcher:
            matcher = opnm(self.base_directory, self.data_dump)
            matcher.calculate_correlation()
            matcher.save_results()

        staged = dp(self.read_correlation_result, self.save_to_gaussian_stage)
        staged.run()

        all_data = AllData(self.db_bath)
        all_data.join()
        all_data.map_to_imges()

        with open(self.save_to_gaussian_stage, 'r') as file:
            data = json.load(file)

        gussians = []
        for x, v in data.items():
            path1, path2 = v.keys()
            path_to_pnu = os.path.dirname(x) + PNU
            path_to_the_Highest = os.path.dirname(path2)
            path_to_second_eighest = os.path.dirname(path1)
            gussians.append(TwoGaussian(path_to_pnu, path_to_the_Highest, path_to_second_eighest))

        print('Data Initialized')
        for i, g in enumerate(gussians, start=1):
            g.init_data(all_data)
            g.create_two_gussians()
            print(f'{i}: TWO-Gaussian Created..')
            g.stage_for_json()

            # Save each TwoGaussian result to JSON
            self.dump_to_json([g.get_results()], self.save_to_gaussian, append=True)
            print(f'{i}: Data staged and saved to JSON')

if __name__ == '__main__':
    args = CameraImageMatcher.parse_arguments()
    matcher = CameraImageMatcher(args)
    matcher.run()
