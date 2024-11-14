from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        new_size = get_next_size()
        new_table = [None]*new_size
        old_table = self.table

        self.table_bucket = new_size
        self.table = new_table
        self.count_node = 0

        # if self.collision_type == "Chain":
        #     for item in old_table:
        #         if item is not None:
        #             for key in item:
        #                 super().insert(key)

        for item in old_table:
            if item is not None:
                if self.collision_type == "Chain":
                    for key in item:
                        self.insert(key)
                else:
                    self.insert(item)

        # else:
        #     for item in old_table:
        #         if item is not None:
        #             super().insert(item)
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        new_size = get_next_size()
        new_table = [None]*new_size
        old_table = self.table

        self.table_bucket = new_size
        self.table = new_table
        self.count_node = 0

        for item in old_table:
            if item is not None:
                if self.collision_type == "Chain":
                    for key in item:
                        self.insert(key)
                else:
                    self.insert(item)


        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()