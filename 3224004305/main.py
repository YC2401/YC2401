import re

# 优化1：正则预编译（放到全局，只编译1次）
# 示例清洗正则，按你原来preprocess里的规则修改pattern
pattern = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9]')


def preprocess(text: str) -> str:
    """文本预处理：过滤非中英数字字符"""
    # 直接复用已经预编译好的正则对象，不再调用re.compile
    cleaned = pattern.sub("", text)
    return cleaned


def ngram_segment(text: str, n: int = 3) -> set:
    """n-gram分词，返回集合用于相似度计算"""
    grams = set()
    if len(text) < n:
        grams.add(text)
        return grams
    for i in range(len(text) - n + 1):
        grams.add(text[i:i + n])
    return grams


def calc_similarity(text1: str, text2: str) -> float:
    """计算两段文本的n-gram重复率（Jaccard）"""
    set1 = ngram_segment(text1)
    set2 = ngram_segment(text2)
    inter = set1 & set2
    union = set1 | set2
    if len(union) == 0:
        return 0.0
    return len(inter) / len(union)


# 优化2：IO优化，一次性读取文件
def read_file(path: str) -> str:
    """读取文本文件，只打开一次"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_answer(result_path: str, sim: float):
    """写入结果"""
    with open(result_path, "w", encoding="utf-8") as f:
        f.write(f"重复率：{sim:.2f}")


def main():
    import sys
    if len(sys.argv) != 4:
        print("用法：python main.py file1.txt file2.txt result.txt")
        return
    file1, file2, outfile = sys.argv[1], sys.argv[2], sys.argv[3]

    # IO优化：一次性读入两个文件
    raw1 = read_file(file1)
    raw2 = read_file(file2)

    # 预处理
    clean1 = preprocess(raw1)
    clean2 = preprocess(raw2)

    # 计算相似度
    sim = calc_similarity(clean1, clean2)
    print(f"计算完成，重复率：{sim:.2f}，结果写入{outfile}")

    # 输出结果
    write_answer(outfile, sim)


if __name__ == "__main__":
    main()
