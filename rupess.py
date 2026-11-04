import ruppess
print("=====Currency Converter=====")
print("1.Rupees to USD doller \n2.USD doller to Rupees \n3.Exit")
while True:
    ch=int(input("\nEnter Choice"))
    if ch==1:
        ruppess.rstodollar()

    elif ch==2:
        ruppess.dollartors()

    elif ch==3:
        print("Exit")
        break;
    else:
        print("Enter Valid Option")
