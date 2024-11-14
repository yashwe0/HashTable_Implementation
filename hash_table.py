from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with Chain
            "Linear"    : Use hashing with Linear probing
            "Double"    : Use Double hashing
        '''
        self.collision_type = collision_type
        self.z = params[0] if self.collision_type in ["Chain", "Linear"] else None
        self.z1 = params[0] if self.collision_type == "Double" else None
        self.z2 = params[1] if self.collision_type == "Double" else None
        self.c2 = params[2] if self.collision_type == "Double" else None
        self.table_bucket = params[-1]
        self.table = [None]*self.table_bucket
        self.count_node=0

    def iter(self):
        l = []
        if self.collision_type == "Chain":
            for i in range(self.table_bucket):
                if self.table[i] is not None:
                    #print(self.table[i])
                    for j in self.table[i]:
                        l.append(j)

        else:
            for i in range(self.table_bucket):
                if self.table[i] is not None:
                    l.append(self.table[i])

        return l

    def char_val(self, char):
        if 'a'<=char<='z':
            return ord(char)- ord('a')
    
        elif 'A'<=char<='Z':
            return ord(char)- ord('A') + 26
        
        elif '0'<=char<='9':
            return int(char)
        else:
            raise ValueError("Unsupported character in key")
        
    def poly_hash(self,key,z):
        h = 0

        for i,char in enumerate(reversed(key)):
            #print(char)
            p_val = self.char_val(char)
            h = h*z + p_val
            # h += p_val*(z**i)
            
        return h
    
    def insert(self, x):
        if self.collision_type == "Chain":
            slot = self.get_slot(x)
            if self.table[slot] is None:
                self.table[slot] = []
            
            if x not in self.table[slot]:
                self.table[slot].append(x)
                self.count_node +=1 

        elif self.collision_type == "Linear":
            slot = self.get_slot(x)
            initial_slot = slot
            while self.table[slot] is not None:
                if self.table[slot] == x:
                    return

                slot = (slot+1)%self.table_bucket
                if slot == initial_slot:
                    raise Exception("Hash table is full")
                    # self.rehash()
                    # self.insert(x)

            self.table[slot] = x
            self.count_node+=1

            

        
        elif self.collision_type == "Double":
            h1,h2 = self.get_slot(x)
            slot = h1
            while self.table[slot] is not None:
                if self.table[slot] == x:
                    return 
                slot = (slot + h2)%self.table_bucket
            
            self.table[slot] = x
            self.count_node +=1

        # if self.get_load()>0.9:
        #     self.rehash()

    

    def find(self, key):
        if self.collision_type == "Chain":
            slot = self.get_slot(key)
            if self.table[slot] is not None and key in self.table[slot]:
                return True
            return False
        elif self.collision_type=="Linear":
            slot = self.get_slot(key)
            init_slot=slot
            while self.table[slot] is not None:
                if self.table[slot] == key:
                    return True
                slot = (slot+1)%self.table_bucket
                if slot==init_slot:
                    break
            return False
        
        elif self.collision_type == "Double":
            h1,h2 = self.get_slot(key)
            slot = h1
            while self.table[slot] is not None:
                if self.table[slot] == key:
                    return True
                slot = (slot+h2)%self.table_bucket

            return False
    
    def get_slot(self, key):
        if self.collision_type== "Double":
            h1 = self.poly_hash(key,self.z1)%self.table_bucket
            h2 = self.c2 - (self.poly_hash(key,self.z2)%self.c2)
            return h1,h2
        else:
            #print("here ::", self.poly_hash(key, self.z)%self.table_bucket)
            #print(self.table_bucket)
            return self.poly_hash(key,self.z)%self.table_bucket
    
    def get_load(self):
        return self.count_node/self.table_bucket
    
    def __str__(self):
        res = []
        for s in self.table:
            if s is None:
                res.append("<EMPTY>")
            elif self.collision_type == "Chain":
                res.append(" ; ".join(str(k) for k in s))
            else:
                res.append(str(s))
        return " | ".join(res)
    
    def printer(self):
        res = []
        for s in self.table:
            if s is None:
                continue
            elif self.collision_type == "Chain":
                res.append(" ; ".join(str(k) for k in s))
            else:
                res.append(str(s))
        return " | ".join(res)

    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
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
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, key):
        super().insert(key)

    def find(self, key):
        return super().find(key)
    
    def get_slot(self, key):
        return super().get_slot(key)
    
    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        return super().__str__()
    
class HashMap(HashTable):
    
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, x):
        # x = (key, value)
 
        if self.collision_type == "Chain":
            slot = self.get_slot(x[0])  # Get the slot using the key part (x[0])
            if self.table[slot] is None:
                self.table[slot] = []  # Initialize the chain (list) if empty

            # Check if the key already exists in the chain, and update the value if it does
            for idx, (k, v) in enumerate(self.table[slot]):
                if k == x[0]:
                    self.table[slot][idx] = x  # Update the (key, value) pair
                    return

            # If key does not exist, append the (key, value) pair
            self.table[slot].append(x)
            self.count_node += 1 

            # if self.get_load() > 0.5:
            #     self.rehash()

        elif self.collision_type == "Linear":
            slot = self.get_slot(x[0])
            initial_slot = slot

            while self.table[slot] is not None:
                if self.table[slot][0] == x[0]:
                    return

                slot = (slot+1) % self.table_bucket
                if slot == initial_slot:
                    # Raise an exception or rehash when the table is full
                    # self.rehash()
                    raise Exception("Table is filled completely.")
                    # self.insert(x)
                    # return

            self.table[slot] = x
            self.count_node += 1

            # if self.get_load() > 0.7:
            #     self.rehash()

        elif self.collision_type == "Double":
            h1, h2 = self.get_slot(x[0])
            slot = h1
            while self.table[slot] is not None:
                if self.table[slot][0] == x[0]:
                    return
                slot = (slot + h2) % self.table_bucket

            self.table[slot] = x
            self.count_node += 1

            # if self.get_load() > 0.7:
            #     self.rehash()

    def find(self, key):
        if self.collision_type == "Chain":
            slot = self.get_slot(key)
            if self.table[slot] is not None:
                # Traverse the chain (list) to find the key
                for k, v in self.table[slot]:
                    if k == key:
                        return v  # Return the value associated with the key
            return None

        elif self.collision_type == "Linear":
            slot = self.get_slot(key)
            init_slot = slot
            while self.table[slot] is not None:
                if self.table[slot][0] == key:
                    return self.table[slot][1]  # Return the value associated with the key
                slot = (slot + 1) % self.table_bucket
                if slot == init_slot:
                    break
            return None

        elif self.collision_type == "Double":
            h1, h2 = self.get_slot(key)
            slot = h1
            while self.table[slot] is not None:
                if self.table[slot][0] == key:
                    return self.table[slot][1]  
                slot = (slot + h2) % self.table_bucket

            return None


    
    
    def get_slot(self, key):
        return super().get_slot(key)
    
    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        res = []
        for s in self.table:
            if s is None:
                res.append("<EMPTY>")
            elif self.collision_type == "Chain":
                res.append(" ; ".join(str(k) for k in s))
            else:
                res.append(str(s))
        return " | ".join(res)
    

def main():
    # Example usage of HashSet with Linear Probing
    # print("HashSet Example with Linear Probing:")
    params_Linear = (31, 7)  # Params: z (for poly hash) and initial table size
    hash_set_Linear = HashSet(collision_type="Linear", params=params_Linear)
    hash_map_Linear = HashMap(collision_type="Linear", params=params_Linear)
    
    hash_set_Linear.insert("apple")
    hash_map_Linear.insert(("apple",10))
    hash_set_Linear.insert("banana")
    hash_map_Linear.insert(("banana",20))
    hash_set_Linear.insert("cherry")
    hash_map_Linear.insert(("cherry",10))
    
    # print("HashSet after insertions (Linear Probing):")
    print(hash_set_Linear)
    print(hash_map_Linear)

    print(f"Find 'banana': {hash_set_Linear.find('banana')}")
    print(f"Find 'grape': {hash_set_Linear.find('grape')}\n")

    # Example usage of HashSet with Chain
    # print("HashSet Example with Chain:")
    params_Chain = (31, 5)  # Params: z (for poly hash) and initial table size

    hash_set_Chain = HashSet(collision_type="Chain", params=params_Chain)
    # print(f"Bucket size :: {params_Chain[-1]}")

    i=1
    
    if i ==1:
        hash_set_Chain.insert("dog")
        print("inserted dog")
        i+=1

    if i==2:
        hash_set_Chain.insert("cat")
        print("inserted cat")
        i+=1

        
    if i==3:
        hash_set_Chain.insert("fish")
        print("inserted fish")
        i+=1

    

    
    
    
    
    # print("HashSet after insertions (Chain):")
    print(hash_set_Chain)

    print(f"Find 'dog': {hash_set_Chain.find('dog')}")
    print(f"Find 'bird': {hash_set_Chain.find('bird')}\n")

    # # Example usage of HashMap with Double Hashing
    # print("HashMap Example with Double Hashing:")
    params_Double = (31, 37, 7, 11)  # Params: z1, z2, c2, and initial table size
    hash_map_Double = HashMap(collision_type="Double", params=params_Double)
    
    hash_map_Double.insert(("dog", 10))
    hash_map_Double.insert(("cat", 20))
    hash_map_Double.insert(("fish", 30))
    
    # print("HashMap after insertions (Double Hashing):")
    print(hash_map_Double)

    print(f"Find key 'dog': {hash_map_Double.find('dog')}")
    print(f"Find key 'horse': {hash_map_Double.find('horse')}")

if __name__ == "__main__":
    main()
