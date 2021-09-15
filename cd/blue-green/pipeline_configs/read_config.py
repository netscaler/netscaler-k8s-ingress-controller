import argparse
import json


class TerraformInputGenerator(object):
    @staticmethod
    def populate_env(input_params):
        print(input_params)
        if input_params.action == 'delete':
            print('##vso[task.setvariable variable=TEARDOWN_FLAG]True')
        with open(input_params.config_file) as json_file:
            json_data = json.load(json_file)
            print(json_data)
            if json_data.keys():
                for param, value in json_data.iteritems():
                    print('##vso[task.setvariable variable={}]{}'.format(param, value))


def main(input_params):
    TerraformInputGenerator.populate_env(input_params)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Terraform input generator')
    parser.add_argument('--config_file', nargs='?', default=None,
                        help='config.json path')
    parser.add_argument('--action', nargs='?', default=None,
                        help='create/delete')
    return parser.parse_args()


if __name__ == "__main__":
    try:
        arguments = parse_arguments()
        main(arguments)
    except Exception as e:
        print('Exception occurred with error: {}'.format(e))