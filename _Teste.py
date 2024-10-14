for i in range(1, 51):
    xpath_SO_Num = f"//*[@id='salesOrderDataTable']/tbody/tr[{i}]/td[2]"
    xoath_Status = f"//*[@id='salesOrderDataTable']/tbody/tr[{i}]/td[5]"

    print(xoath_Status)
    print(xpath_SO_Num)