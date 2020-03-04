import zhconv


def to_zh_cn(arr):
    if isinstance(arr, dict):
        return {to_zh_cn(key): to_zh_cn(val) for key, val in arr.items()}
    if isinstance(arr, list):
        return [to_zh_cn(val) for val in arr]
    if isinstance(arr, str):
        return zhconv.convert(arr, 'zh-hans')
    return arr



