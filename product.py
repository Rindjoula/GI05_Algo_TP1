import random 

class Product:
    def __init__(self, id, provider, name, price, units):
        """
        Parameters:
            id(int): product's id 
            provider(Provider): provider object which sells the product
            name(string): name of the product
            price(int): price of one unit of the product
            units(int): number of available products 
        """

        self.id = id 
        self.provider = provider
        self.name = name
        self.price = price
        self.units = units

def feed_products(providers, N):
    """
    Parameters:
        providers(Provider[]): list of providers
        N(int): number of products; must be >= number of providers
    Returns:
        (Product[]) list of N Product objects
    """

    if N < len(providers):
        print("There should be at least " + len(providers) + " products.")
        exit(1)

    list_products = []
    for i in range(N):
        name = str(i) + "-product"
        id_provider = random.randint(0, len(providers)-1)
        provider = providers[id_provider]
        price = random.randint(1, 100)
        units = random.randint(1, 20)
        product = Product(i, provider, name, price, units)
        list_products.append(product)

    return list_products

def write_products(filename, products):
    """
    Parameters:
        filename(string): name of the file to write the products
        products(Product[]): list of Product objects
    """

    HEAD = "id\tname\tprovider\tprice\tunits"

    with open(filename, "w") as f:
        f.write(HEAD)
        f.write("\n")
        for product in products:
            p = str(product.id) + "\t" + product.name + "\t" + str(product.provider.id) + "\t" + str(product.price) + "\t" + str(product.units)
            f.write(p)
            f.write("\n")

def feed_T_matrice(list_products):
    """
    Parameters:
        list_products(Product[]): list of Product objects
    Returns:
        matrix T, N*N dimensions, where N is the number of Product objects
        if T[i][j] = 1 that means that products i and j were bought at the same time; 0 otherwise
    """

    N = len(list_products)

    T = []
    
    for i in range(N):
        tmp = []
        for j in range(N):
            if i < j:
                r= random.random()
                if r < 0.2:
                    tmp.append(1)
                else:
                    tmp.append(0)
            elif i == j:
                tmp.append(1)
            else:
                tmp.append(T[j][i])
        T.append(tmp)

    return T

def write_matrice(filename, T):
    """
    Parameters:
        filename(string): name of the file to write the T matrix
        T(matrix N*N): matrix returned by feed_T_matrix function
    """

    with open(filename, "w") as f:
        N = len(T)
        f.write(str(N))
        f.write("\n")
        for i in range(N):
            for j in range(N):
                f.write(str(T[i][j]))
                f.write("\t")
            f.write("\n")

def get_products(filename):
    """
    Parameters:
        filenmame(string): name of the file where are stored the products

    Returns:
        dictionary of products: key = id of the product / value = Product object
    """

    dict_products = {}
    with open(filename, "r") as f:
        header = f.readline()
        header = header.split("\t")
        for line in f.readlines():
            line_split = line.split("\t")
            id = line_split[0]
            name = line_split[1]
            provider = line_split[2]
            price = line_split[3]
            units = line_split[4]
            product = Product(id, provider, name, price, units)
            dict_products[id] = product

    return dict_products

def feed_B_matrice(T):
    """
    Parameters:
        T(matrix N*N): matrix T returned by feed_T_matrix function
    Returns:
        matrix B, N*N dimensions, where N is the number of Product objects
    """
    N = len(T)

    B = []

    for i in range(N):
        tmp = []
        for j in range(N):
            if i < j:
                if T[i][j] == 1:
                    nb = random.randint(1, 100)
                    tmp.append(nb)
                else:
                    tmp.append(0)
            elif i == j:
                tmp.append(0)
            else:
                tmp.append(B[j][i])
                
        B.append(tmp)

    return B

def read_matrice_from_file(filename):
    M = []

    with open(filename, "r") as f:
        nb = int(f.readline())
        for i in range(nb):
            tmp = []
            line = f.readline().split("\t")
            for j in range(nb):
                tmp.append(int(line[j]))
            M.append(tmp)
    return M