import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary:
    # IMPLEMENT ALL FUNCTIONS HERE
    
    def __init__(self, book_titles, texts):
        self.books = []
        
        for title, text in zip(book_titles, texts):
            # Join the list of words to form a single string
            words = text
            sorted_words = self.merge_sort(words)
            distinct_words = self.get_dis(sorted_words)
            self.books.append((title, sorted_words, distinct_words))

        self.books = self.merge_sort(self.books)

    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        return self.merge(left, right)

    def merge(self, left, right):
        sorted_arr = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                sorted_arr.append(left[i])
                i += 1
            else:
                sorted_arr.append(right[j])
                j += 1
        sorted_arr.extend(left[i:])
        sorted_arr.extend(right[j:])
        return sorted_arr

    def bs(self, title):
        low = 0
        high = len(self.books) - 1

        while low <= high:
            mid = (low + high) // 2
            if self.books[mid][0] == title:
                return mid
            elif self.books[mid][0] < title:
                low = mid + 1
            else:
                high = mid - 1
        return -1 

    def binary_search(self, arr, keyword):
        low = 0
        high = len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == keyword:
                return True
            elif arr[mid] < keyword:
                low = mid + 1
            else:
                high = mid - 1
        return False

    def get_dis(self, sorted_arr):
        distinct = []
        if not sorted_arr:
            return distinct
        distinct.append(sorted_arr[0])
        for i in range(1, len(sorted_arr)):
            if sorted_arr[i] != sorted_arr[i - 1]:
                distinct.append(sorted_arr[i])
        return distinct            

    def distinct_words(self, book_title):
        idx = self.bs(book_title)
        if idx != -1:
            return self.books[idx][2]
        return []

    def count_distinct_words(self, book_title):
        idx = self.bs(book_title)
        if idx != -1:
            return len(self.books[idx][2])
        return 0
    
    def search_keyword(self, keyword):
        result = []
        for title, sorted_words, _ in self.books:
            if self.binary_search(sorted_words, keyword):
                result.append(title)
        return result

    def print_books(self):
        for title, sorted_words, distinct_words in self.books:
            # dis = self.merge_sort(distinct_words)
            distinct_words_str = " | ".join(distinct_words)
            print(f"{title}: {distinct_words_str}")

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        self.name = name
        self.books= []
        self.z = None
        self.params = params
    
        if name == "Jobs":
            self.z = "Chain"
            self.book_text = ht.HashMap(self.z,params)
            # self.book_titles = ht.HashSet(self.z, params)
        elif name == "Bezos":
            self.z = "Double"
            self.book_text = ht.HashMap(self.z,params)
            # self.book_titles = ht.HashSet(self.z, params)
        elif name == "Gates":
            self.z = "Linear"
            self.book_text = ht.HashMap(self.z,params)
            # self.book_titles = ht.HashSet(self.z, params)
        else:
            raise ValueError("Invalid library name. Choose from 'Jobs', 'Gates', or 'Bezos'")
    
    def add_book(self, book_title, text):
        #print(text)
        textie = ht.HashSet(self.z, self.params)
        #print(text)
        for i in text:
            textie.insert(i)
        self.book_text.insert((book_title, textie))
    
    def distinct_words(self, book_title):
        s = self.book_text.find(book_title)
        l = s.iter()
        #print(l)
        
        return l
    
    def count_distinct_words(self, book_title):
        s = self.book_text.find(book_title)
        return (s.count_node)
    
    def search_keyword(self, keyword):
        l = []

        for i in self.book_text.iter():
            j = i[1]
            p = j.find(keyword)
            if p:
                l.append(i[0])

        #print(l)

        return l
    
    def print_books(self):
        
        for i in self.book_text.iter():
            #print(i[1])
            # (print(i[1]))
            print(f"{i[0]}: {(i[1])}")