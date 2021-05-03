import time
from iol_request import get_ggal,log_in
from concurrent.futures import ThreadPoolExecutor


def get_spot_Rfx20(bearer_token):
    composicion = {"ALUA":63.746460,
                    "BBAR":16.597189,
                    "BMA":33.692701,
                    "BYMA":5.757708,
                    "CEPU":67.836129,
                    "COME":252.553591,
                    "CRES":26.149783,
                    "EDN":30.224442,
                    "GGAL":92.756774,
                    "LOMA":23.627009,
                    "MIRG":1.355641,
                    "MORI":2.901807,
                    "PAMP":85.780111,
                    "SUPV":23.991923,
                    "TECO2":10.128165,
                    "TGNO4":7.115384,
                    "TGSU2":12.550024,
                    "TXAR":55.665327,
                    "VALO":67.905858,
                    "YPFD":15.528096}

    t1 = time.time()
    result = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for i in list(composicion.keys()):
            executor.submit(lambda:result.append(get_ggal(bearer_token,i)*composicion[i]))
        time.sleep(1)
    t2 = time.time()
    print("20 requests en {} segundos.".format(t2 - t1))
    return sum(result)

bearer_token, refresh_token = log_in()
print(get_spot_Rfx20(bearer_token))
