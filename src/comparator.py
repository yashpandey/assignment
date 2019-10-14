from utils import utils
import csv


class Comparator:

    def import_file1(self, file1):
        """
        This function will import the csv file
        :param file1: file name to be imported
        :return: api endpoints present at the csv file
        """
        with open(file1) as csvDataFile:
            csvReader = csv.DictReader(csvDataFile)
            for line in csvReader:
                yield line.get('api1')

    def import_file2(self, file2):
        """
        This function will import the csv file
        :param file1: file name to be imported
        :return: api endpoints present at the csv file
        """
        with open(file2) as csvDataFile:
            csvReader = csv.DictReader(csvDataFile)
            for line in csvReader:
                yield line.get('api1')

    def make_end_points_dict(self, file1, file2):
        """
        :param file1:Name of the csv file to be imported
        :param file2:Name of the csv file to be imported
        :return: True or false depending on the response is equal or not.
        """
        file_one_end_point_dict = {}
        file_two_end_point_dict = {}
        line_no = 1
        for i in self.import_file1(file1):
            file_one_end_point_dict[line_no] = i
            line_no += 1

        line = 1
        for i in self.import_file2(file2):
            file_two_end_point_dict[line] = i
            line += 1

        return self.get_end_points(file_one_end_point_dict, file_two_end_point_dict)

    def get_end_points(self, dict1, dict2):
        """

        :param dict1: Dictionary generated from the first file
        :param dict2: Dictionary generated from the second file
        """
        for i in dict1:
            try:
                return self.compare_api_response(dict1[i], dict2[i])
            except IndexError:
                print('Out of index')

    def compare_api_response(self, end_point1, end_point2):
        """
        This method will compare the two endpoints and returns True if they are equal
        :param end_point1: api endpoint from the first file
        :param end_point2: api endpoint from the second file
        :return:
        """
        response1 = utils.get(end_point1)
        response2 = utils.get(end_point2)
        if self.ordered(response1) == self.ordered(response2):
            return True
        else:
            return False

    def ordered(self, obj):
        """
        Returns a ordered dict
        """
        if isinstance(obj, dict):
            return sorted((k, self.ordered(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(self.ordered(x) for x in obj)
        else:
            return obj


if __name__ == '__main__':
    obj = Comparator()
    obj.make_end_points_dict('abc.csv','xyz.csv')
