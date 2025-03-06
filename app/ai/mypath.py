class Path(object):
    @staticmethod
    def db_root_dir(dataset):
        if dataset == 'simple':
            return '/path/to/datasets/simple/'
        else:
            print('Dataset {} not available.'.format(dataset))
            raise NotImplementedError
