instancePrices = {
    "us-east": {
        "large": 0.12,
        "xlarge": 0.23,
        "2xlarge": 0.45,
        "4xlarge": 0.774,
        "8xlarge": 1.4,
        "10xlarge": 2.82
    },
    "us-west": {
        "large": 0.14,
        "2xlarge": 0.413,
        "4xlarge": 0.89,
        "8xlarge": 1.3,
        "10xlarge": 2.97
    }
}


class ResourceAllocator:
    def __init__(self):
        self.instance_price = {}
        self.instance_cpus = {}
        self.total_cost = 0
        self.server = []
        self.output = []

    def lowestPriceCalculator(self, instPrice):
        for i in list(instPrice.keys()):
            instPrice[i] = instPrice[i]/self.instance_cpus[i]
        instPricelist = sorted(instPrice.items(), key=lambda x: x[1])
        self.instance_price = dict(instPricelist)

    def calculateServerPrice(self, cpus, location, hours):
        for i in list(self.instance_price.keys()):
            cpuNeed = cpus // self.instance_cpus[i]
            if(cpuNeed != 0):
                if(i in instancePrices[location]):
                    cpus -= cpuNeed * self.instance_cpus[i]
                    self.total_cost += ((instancePrices[location]
                                         [i]) * hours) * cpuNeed
                    self.server.append((i, cpuNeed))
        self.outputFormatter(location)

    def setters(self):
        self.instance_price = {}
        self.total_cost = 0
        self.server = []

    def outputFormatter(self, location):
        op = {
            "region": location,
            "total_cost": "$%.2f" % self.total_cost,
            "server": self.server
        }
        self.output.append(op)

    def calculatePriceServer(self, price, hours, location):
        self.total_cost = 0
        for i in list(self.instance_price.keys()):
            cpuNeed = int(price // (instancePrices[location][i] * hours))
            if(cpuNeed != 0):
                self.total_cost += cpuNeed * \
                    (instancePrices[location][i] * hours)
                self.server.append((i, cpuNeed))
                price -= cpuNeed * (instancePrices[location][i] * hours)
        self.outputFormatter(location)

    def get_costs(self, **kwargs):
        self.instance_cpus = kwargs["instances"]
        self.output = []
        if("cpus" in kwargs and "hours" in kwargs):
            for i in list(instancePrices.keys()):
                self.setters()
                self.lowestPriceCalculator(instancePrices[i].copy())
                self.calculateServerPrice(kwargs["cpus"], i, kwargs["hours"])

        elif("price" in kwargs and "hours" in kwargs):
            for i in list(instancePrices.keys()):
                self.setters()
                self.lowestPriceCalculator(instancePrices[i].copy())
                self.calculatePriceServer(kwargs["price"], kwargs["hours"], i)
        print(self.output)


def main():
    instanceCpus = {
        "large": 1,
        "xlarge": 2,
        "2xlarge": 4,
        "4xlarge": 8,
        "8xlarge": 16,
        "10xlarge": 32,
    }

    resourceAllocator = ResourceAllocator()
    print("Testcase: 1")
    resourceAllocator.get_costs(
        cpus=129, hours=5.080367, instances=instanceCpus)
    print("\n\n\nTestcase: 2")
    resourceAllocator.get_costs(
        price=44.4, hours=5.087, instances=instanceCpus)


if(__name__ == "__main__"):
    main()
