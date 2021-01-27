"""
Global Variable as per Flipkart chart of commission
"""

WEIGHT_SLAB = ['0.0-0.5', '0.5-1.0', '1.0-1.5', '1.5-2.0', '2.0-3.0', '3.0-12.0', '>12.0']
LOCAL = [40, 4, 13, 10, 8, 7, 4]
ZONAL = [47, 19, 17, 18, 11, 10, 5]
NATIONAL = [60, 26, 28, 22, 17, 16, 8]

WEIGHT_LIST = None


def cal_payment(weight, zone, tiers) -> float:
    """
    This Function will take weight and zone
    and calculate the price as the the zone
    :param weight:
    :param zone:
    :return: price
    """
    print(weight, zone, tiers, sep='---')
    global WEIGHT_LIST
    slab, weight = check_slab(weight)
    multiply_factor = 1
    if slab and weight:
        try:
            index = WEIGHT_SLAB.index(slab)
            PRICE = 0.0
            #  Check for the Zone
            if zone.lower() == 'local':
                WEIGHT_LIST = LOCAL
            elif zone.lower() == 'zonal':
                WEIGHT_LIST = ZONAL
            elif zone.lower() == 'national':
                WEIGHT_LIST = NATIONAL
            else:
                pass

            for i, v in enumerate(WEIGHT_SLAB[: index + 1]):
                if weight > 0.0 and v != '2.0-3.0' and v != '3.0-12.0' and v != slab:
                    PRICE += float(WEIGHT_LIST[i]) * float(multiply_factor)
                    weight -= 0.5 * multiply_factor
                elif v == '2.0-3.0' and weight > 0.0 and v != slab and v != '3.0-12.0':
                    multiply_factor = 2
                    PRICE += float(WEIGHT_LIST[i]) * float(multiply_factor)
                    weight -= (0.5 * multiply_factor)
                elif v == '3.0-12.0':
                    if weight >= 9.0:
                        multiply_factor = 9.0
                        PRICE += float(WEIGHT_LIST[i]) * float(multiply_factor)
                        weight -= 9.0
                        i += 1
                    if weight > 0.0:
                        v = WEIGHT_SLAB[-1]
                        multiply_factor = weight
                        PRICE += float(WEIGHT_LIST[i]) * float(multiply_factor)
                else:
                    PRICE += float(WEIGHT_LIST[i]) * float(multiply_factor)

            #  check for the tiers

            if tiers.lower() == 'bronze':
                return PRICE
            elif tiers.lower() == 'gold':
                return PRICE * 0.8
            elif tiers.lower() == 'silver':
                return PRICE * 0.9
        except Exception as e:
            print("CALCULATOR" + str(e))


def check_slab(weight) -> tuple:
    """
    This function will take weight from the user and calculate the weight
    :param weight: user will give
    :return: object
    """
    if weight:
        if (float(weight) >= 0.0) and (float(weight) <= 0.5):
            slab = '0.0-0.5'
            return slab, weight

        elif (float(weight) >= 0.5) and (float(weight) <= 1.0):
            slab = '0.5-1.0'
            return slab, weight

        elif (float(weight) >= 1.0) and (float(weight) <= 1.5):
            slab = '1.0-1.5'
            return slab, weight

        elif (float(weight) >= 1.5) and (float(weight) <= 2.0):
            slab = '1.5-2.0'
            return slab, weight

        elif (float(weight) >= 2.0) and (float(weight) <= 3.0):
            slab = '2.0-3.0'
            return slab, weight

        elif (float(weight) >= 3.0) and (float(weight) <= 12.0):
            slab = '3.0-12.0'
            return slab, weight

        else:
            slab = '>12.0'
            return slab, weight
    else:
        print("Weight None")
        return None, None


