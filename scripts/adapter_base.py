from abc import ABC, abstractmethod


class StorageAdapter(ABC):

    @abstractmethod
    def read_item(self, item_id):
        pass

    @abstractmethod
    def write_item(self, item_id, data):
        pass

    @abstractmethod
    def list_items(self, filter_dict=None):
        pass

    @abstractmethod
    def get_health(self):
        pass
