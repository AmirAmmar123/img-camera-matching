from joinData import AllData
from gaussian import GaussianPairs
import os 
from const import PNU_DIR 
import json 
from pnuidmapper import Mapper as mp 
from optimized_averging_training_pnu import PNUMatcher as opnm
from preparing_data_for_gaussian_thresholding import PreProcessorToThreshold as pptt 
from mylogger import Logger
class CameraImageMatcher:
    def __init__(self, args, logger:Logger):
        self.db_path = args.db_path
        self.data_dump = args.data_dump
        self.home_directory_path = args.home_directory_path
        self.read_correlation_result = args.read_correlation_result
        self.save_to_gaussian_stage = args.save_to_gaussian_stage
        self.save_to_gaussian = args.save_to_gaussian
        self.create_x_pnu_id = args.create_x_pnu_id
        self.activate_creation = args.activate_creation
        self.activate_matcher = args.activate_matcher
        self.logger = logger

    def dump_to_json(self, data, file_path):

        with open(file_path, 'a+') as f:

            f.seek(0)

            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
 
                existing_data = []

            existing_data.append(data)


            f.seek(0)
            f.truncate()

            json.dump(existing_data, f,indent=4)

            print(f'Data successfully written to {file_path}')



    def run(self):
        self.logger.info("Running Camera Image Matching Function...")
        if self.activate_creation:
            for id in range(self.create_x_pnu_id):
                self.logger.info(f'Creating pnu_id using the testing data-set {id+1}...')
                mp_instance = mp(self.db_path, id, self.logger)
                mp_instance.transform_all_imges()
                mp_instance.create_ID().saveID()

        if self.activate_matcher:
            matcher = opnm(self.db_path, self.data_dump, self.logger)
            matcher.calculate_correlation()
            matcher.save_results()

        staged = pptt(self.read_correlation_result, self.save_to_gaussian_stage, self.logger)
        staged.run()

        all_data = AllData(self.db_path, self.logger)
        all_data.join()
        all_data.map_to_imges()

        with open(self.save_to_gaussian_stage, 'r') as file:
            self.logger.info(f'Loading {self.save_to_gaussian_stage}')
            data = json.load(file)

        gussians = []
        for x, v in data.items():
            path1, path2 = v.keys()
            path_to_pnu = os.path.dirname(x)+ '/' + PNU_DIR
            path_to_the_Highest = os.path.dirname(path2)
            path_to_second_eighest = os.path.dirname(path1)
            gussians.append(GaussianPairs(path_to_pnu, path_to_the_Highest, path_to_second_eighest, self.logger))

        self.logger.info(f'Ready to create {len(gussians)} pairs of Gaussian...')
        for i, g in enumerate(gussians, start=1):
            g.init_data(all_data)
            g.create_two_gussians()
            self.logger.info(f'Pair #{i} Created...')
            self.dump_to_json(g.get_results(), self.save_to_gaussian)
            self.logger.info(f'{i}: Data staged and saved to JSON')
        self.logger.info('The processing of Data has been successfully finished')