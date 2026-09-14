import sys

def parse_argv():
    """解析命令行参数，返回三个文件路径"""
    if len(sys.argv) != 4:
        print("参数错误！用法：python main.py 原文路径 抄袭版路径 输出文件路径")
        sys.exit(0)
    orig_path = sys.argv[1]    # 获取原文文件路径
    copy_path = sys.argv[2]    # 获取抄袭版文件路径
    out_path = sys.argv[3]     # 获取结果输出文件路径
    return orig_path, copy_path, out_path


def read_file(file_path):
    """读取文件，返回文件内容，文件不存在返回None"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()  # 读取全部文本
        return content
    except FileNotFoundError:
        print(f"错误：文件不存在 {file_path}")
        return None


def preprocess(text: str):
    """文本预处理，清除换行与空格"""
    text = text.replace("\n", "").replace(" ", "") # 去除换行符、空格
    return text


def ngram_segment(text: str, n: int):
    """n-gram分词，返回片段集合"""
    seg_set = set()
    # 滑动窗口截取连续n个字
    for i in range(len(text) - n + 1):
        seg = text[i:i+n]
        seg_set.add(seg) # 将片段加入集合，自动去重
    return seg_set


def calc_similarity(orig_text: str, copy_text: str, n=2):
    """计算文本重复率，返回重复率浮点数"""
    orig_set = ngram_segment(orig_text, n)       # 原文做2-gram分词
    copy_set = ngram_segment(copy_text, n)      # 抄袭版做2-gram分词
    inter = orig_set & copy_set                 # 求两个集合交集
    rate = len(inter) / len(copy_set)           # 重复率 = 交集数量 / 抄袭片段总数
    return rate


def write_answer(out_path: str, rate: float):
    """将重复率格式化写入输出文件"""
    res = "{:.2f}".format(rate) # 保留两位小数
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(res) # 写入结果到文件


def main():
    """程序主入口，串联完整流程"""
    orig_path, copy_path, out_path = parse_argv() # 获取三个文件路径
    orig_content = read_file(orig_path)           # 读取原文
    copy_content = read_file(copy_path)           # 读取抄袭版

    if orig_content is None or copy_content is None: # 文件读取失败直接退出
        return

    orig_clean = preprocess(orig_content)    # 原文清洗
    copy_clean = preprocess(copy_content)    # 抄袭版清洗
    repeat_rate = calc_similarity(orig_clean, copy_clean) # 计算重复率
    write_answer(out_path, repeat_rate)      # 写入结果


if __name__ == "__main__":
    main() # 启动程序
