from abc import ABC, abstractmethod

from resources.dst_vendor.data_objects import AddressData, AddressSetData, PolicyData, ServiceData, ServiceSetData


class VendorAbc(ABC):
    """This is ABC to create Destination vendor"""

    @abstractmethod
    def service(self, data: ServiceData): ...

    @abstractmethod
    def service_set(self, data: ServiceSetData): ...

    @abstractmethod
    def address(self, data: AddressData): ...

    @abstractmethod
    def address_set(self, data: AddressSetData): ...

    @abstractmethod
    def policy(self, data: PolicyData): ...
