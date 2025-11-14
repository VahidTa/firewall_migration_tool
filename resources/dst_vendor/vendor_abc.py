from abc import ABC, abstractmethod


class VendorAbc(ABC):
    """This is ABC to create Destination vendor"""

    @abstractmethod
    def service(self): ...

    @abstractmethod
    def service_set(self): ...

    @abstractmethod
    def address(self): ...

    @abstractmethod
    def address_set(self): ...

    @abstractmethod
    def policy(self): ...
