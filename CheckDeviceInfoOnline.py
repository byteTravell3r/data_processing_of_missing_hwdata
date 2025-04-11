import wget, csv

PCIeDevInfoTableCSV = "MissingName_PCIe.csv"

WebSite = "https://driverscollection.com/"


def SearchForPCIeDevInfo(_VendorID: str, _ProductID: str) -> str:
    SearchInfo = f"Search/PCI%5CVEN_{_VendorID}%26DEV_{_ProductID}"
    SavePath = f"SearchInDriversCollection/{_VendorID}_{_ProductID}.html"
    Address = WebSite + SearchInfo
    WGetDownloadReturn = wget.download(Address, SavePath)
    return WGetDownloadReturn
    pass


if __name__ == "__main__":
    with open(PCIeDevInfoTableCSV, encoding="utf-8") as TableFile:
        Table = csv.DictReader(TableFile)
        for Row in Table:
            VendorID = Row.get("VendorID").upper()
            ProductID = Row.get("ProductID").upper()
            print(f"Fetching Information Of Device {VendorID}:{ProductID} on {WebSite}")
            Filename = SearchForPCIeDevInfo(VendorID, ProductID)
            print(f"Saved to File {Filename}!")
        pass
    pass
