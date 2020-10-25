



def hasQuerys(wanted, recieved):
    res = {}
    for query in wanted:
        if(query not in recieved):
            return False
        else:
            res[query] = recieved[query][0]
    return res


def main():
    print("started")
    
    print(hasQuerys(["act", "indp"], {"inp":"97","act":"49"}))


if __name__ == "__main__":
    main()
