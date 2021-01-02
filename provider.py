class Provider:
    def __init__(self, id, name):
        """
        Parameters:
            id(int): provider's id 
            name(string): provider's name
        """

        self.id = id
        self.name = name 


def feed_providers(r):
    """
    Parameters:
        r(int): number of providers; must be >= 2
    Returns:
        (Provider[]) list of r Provider objects
    """

    if r < 2: 
        print("There must be at least 2 providers.")
        exit(1)

    list_providers = []
    for i in range(r):
        name = str(i) + "-provider"
        provider = Provider(i, name)
        list_providers.append(provider)
    return list_providers 