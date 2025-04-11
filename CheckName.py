import os

DeviceSearchHtmlFileDir = "./SearchInDriversCollection"
DeviceSearchHtmlFile = ""
NothingKeyword = "Nothing"
SomethingKeyword = "This is Device ID of"
FilesInDirList = os.listdir(DeviceSearchHtmlFileDir)
NotUsefulInformationList = []

for DeviceSearchHtmlFile in FilesInDirList:
    with open(f"{DeviceSearchHtmlFileDir}/{DeviceSearchHtmlFile}", encoding="utf-8") as HtmlFile:
        Remove = False
        VID_PID = DeviceSearchHtmlFile.split(".")[0]
        print(VID_PID, end=', ')
        FileContent = HtmlFile.readlines()
        for Line in FileContent:
            try:
                Line.index(NothingKeyword)
                print(f"None")
                NotUsefulInformationList.append(DeviceSearchHtmlFile)
            except ValueError:
                try:
                    Line.index(SomethingKeyword)
                    InfoLine = Line.split("<br />")[1]
                    print(InfoLine.split("<b>")[1].split("</b>")[0].split(" - ")[0])
                except ValueError:
                    pass
                pass
        pass
    pass

for File in NotUsefulInformationList:
    FilesInDirList.remove(File)

# print("Useful:")
#
# for FileName in FilesInDirList:
#     print(FileName)
#
# print("Not Useful:")
#
# for FileName in NotUsefulInformationList:
#     print(FileName)
#
print("End")